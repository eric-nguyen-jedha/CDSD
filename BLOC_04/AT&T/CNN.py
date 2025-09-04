# Preprocessing NLP
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.lang.en.stop_words import STOP_WORDS as EN_STOP_WORDS

df["SMS_Clean"] = df["SMS"].apply(lambda x: ''.join(ch for ch in x if ch.isalnum() or ch == " " or ch == "'"))
df["SMS_Clean"] = df["SMS_Clean"].apply(lambda x: x.replace(" +", " ").lower().strip())
df["SMS_Clean"] = df["SMS_Clean"].apply(lambda x: " ".join([token.lemma_ for token in nlp(x) if (token.lemma_ not in EN_STOP_WORDS) and (token.text not in EN_STOP_WORDS)]))

# Filtrer les valeurs non-string si nécessaire
mask = df.SMS_Clean.apply(lambda x: type(x) == str)
df = df[mask]

# 🔥 CORRECTION PRINCIPALE: Division AVANT tokenization
from sklearn.model_selection import train_test_split
X_train_text, X_val_text, y_train, y_val = train_test_split(
    df.SMS_Clean, df.Target, test_size=0.3, random_state=42, stratify=df.Target
)

# Tokenization UNIQUEMENT sur les données d'entraînement
import tensorflow as tf
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=20000, oov_token="out_of_vocab")
tokenizer.fit_on_texts(X_train_text)  # ✅ Seulement sur train

# Encodage des données
X_train_encoded = tokenizer.texts_to_sequences(X_train_text)
X_val_encoded = tokenizer.texts_to_sequences(X_val_text)

# Padding
X_train_pad = tf.keras.preprocessing.sequence.pad_sequences(X_train_encoded, padding="post")
X_val_pad = tf.keras.preprocessing.sequence.pad_sequences(X_val_encoded, padding="post", 
                                                         maxlen=X_train_pad.shape[1])
#OverSampling
# 🎛️ PARAMÈTRES - Modifiez selon vos besoins
STRATEGY = "partial"  # "full", "partial", "factor", "none"
TARGET_RATIO = 0.3    # Pour partial: ratio de la classe minoritaire
FACTOR = 3.0          # Pour factor: multiplier la classe minoritaire

# Préparation des données
y_train_array = np.array(y_train)
ham_mask = y_train_array == 0
spam_mask = y_train_array == 1

ham_data, spam_data = X_train_pad[ham_mask], X_train_pad[spam_mask]
ham_labels, spam_labels = y_train_array[ham_mask], y_train_array[spam_mask]

print(f"📊 Original: {len(ham_data)} HAM, {len(spam_data)} SPAM")

# Déterminer la classe minoritaire et calculer les cibles
is_spam_minority = len(spam_data) < len(ham_data)
minority_count = min(len(ham_data), len(spam_data))
majority_count = max(len(ham_data), len(spam_data))

if STRATEGY == "full":
    target_minority = majority_count
elif STRATEGY == "partial":
    target_minority = int(TARGET_RATIO * majority_count / (1 - TARGET_RATIO))
elif STRATEGY == "factor":
    target_minority = int(minority_count * FACTOR)
else:  # "none"
    target_minority = minority_count

# Appliquer le rééquilibrage
if target_minority > minority_count and STRATEGY != "none":
    if is_spam_minority:
        spam_resampled = resample(spam_data, n_samples=target_minority, random_state=42)
        labels_resampled = resample(spam_labels, n_samples=target_minority, random_state=42)
        X_train_balanced = np.vstack([ham_data, spam_resampled])
        y_train_balanced = np.concatenate([ham_labels, labels_resampled])
    else:
        ham_resampled = resample(ham_data, n_samples=target_minority, random_state=42)
        labels_resampled = resample(ham_labels, n_samples=target_minority, random_state=42)
        X_train_balanced = np.vstack([ham_resampled, spam_data])
        y_train_balanced = np.concatenate([labels_resampled, spam_labels])
else:
    X_train_balanced = X_train_pad
    y_train_balanced = y_train_array

# Résultats
final_ham = np.sum(y_train_balanced == 0)
final_spam = np.sum(y_train_balanced == 1)
total = len(y_train_balanced)

print(f"📊 Final: {final_ham} HAM ({final_ham/total*100:.1f}%), {final_spam} SPAM ({final_spam/total*100:.1f}%)")

if STRATEGY != "none" and target_minority > minority_count:
    increase = (target_minority - minority_count) / minority_count * 100
    minority_class = "SPAM" if is_spam_minority else "HAM"
    print(f"📈 {minority_class} augmenté de {increase:.1f}% (×{target_minority/minority_count:.1f})")


# 🔧 CORRECTION 8: Datasets TensorFlow optimisés
BATCH_SIZE = 32  # Réduire la taille de batch
BUFFER_SIZE = 1000

train_dataset = tf.data.Dataset.from_tensor_slices((X_train_balanced, y_train_balanced))
val_dataset = tf.data.Dataset.from_tensor_slices((X_val_pad, y_val))

train_batch = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
val_batch = val_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)


# Modèle avec couche supplémentaire et régularisation

num_filters = 128  # Nombre de filtres par couche CNN
dropout_rate = 0.5

vocab_size = tokenizer.num_words

# Alternative plus simple (à tester en comparaison)
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size + 1, 8, 
                              input_shape=[X_train_pad.shape[1]], name="embedding"),
    tf.keras.layers.GlobalAveragePooling1D(),
     tf.keras.layers.Dense(32, activation='relu'),
     tf.keras.layers.Dropout(0.7),
     tf.keras.layers.Dense(1, activation="sigmoid")
 ])

optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer,
              loss="binary_crossentropy",
              metrics=["accuracy", 
                      tf.keras.metrics.Precision(name="precision"),
                      tf.keras.metrics.Recall(name="recall"),
                      tf.keras.metrics.AUC(name="auc")])

# Callbacks avancés pour l'entraînement
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os

# Créer le dossier pour sauvegarder les modèles
os.makedirs('models', exist_ok=True)

# 1. ModelCheckpoint - Sauvegarde du meilleur modèle
checkpoint = ModelCheckpoint(
    filepath='models/best_spam_model.h5',
    monitor='val_auc',              # Surveille l'AUC (meilleure métrique pour classification binaire)
    mode='max',                     # Maximiser l'AUC
    save_best_only=True,            # Ne sauvegarde que le meilleur
    save_weights_only=False,        # Sauvegarde le modèle complet
    verbose=1                       # Affiche quand il sauvegarde
)

# 2. EarlyStopping - Arrêt anticipé si pas d'amélioration
early_stopping = EarlyStopping(
    monitor='val_loss',             # Surveille la loss de validation
    patience=25,                    # Attend 15 epochs sans amélioration
   restore_best_weights=True,      # Restaure les meilleurs poids à la fin
   verbose=1,
   min_delta=0.001                 # Amélioration minimale considérée significative
)

# 3. ReduceLROnPlateau - Réduction du learning rate
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',             # Surveille la loss de validation
    factor=0.5,                     # Divise le LR par 2
    patience=10,                     # Attend 7 epochs avant réduction
    min_lr=1e-7,                    # LR minimum
    verbose=1,
    cooldown=3                      # Attendre 3 epochs après réduction avant nouvelle réduction
)

# Liste des callbacks
callbacks_list = [checkpoint,
                  early_stopping, 
                  reduce_lr]

print("📋 Configuration des callbacks:")
print(f"  • ModelCheckpoint: Sauvegarde dans 'models/best_spam_model.h5' (métrique: val_auc)")
print(f"  • EarlyStopping: Patience de 15 epochs (métrique: val_loss)")
print(f"  • ReduceLROnPlateau: Réduction LR /2 après 7 epochs sans amélioration")

# Entraînement avec callbacks
history = model.fit(train_batch, 
                    epochs=200, 
                    validation_data=val_batch,
                    callbacks=callbacks_list,
                    verbose=1)

print("\n🎯 Entraînement terminé!")
print("📁 Meilleur modèle sauvegardé dans: 'models/best_spam_model.h5'")

# Charger le meilleur modèle pour évaluation finale
print("\n🔄 Chargement du meilleur modèle pour évaluation...")
best_model = tf.keras.models.load_model('models/best_spam_model.h5')

# Évaluation finale sur les données de validation
print("\n📊 Évaluation du meilleur modèle:")
final_results = best_model.evaluate(val_batch, verbose=0)
metrics_names = best_model.metrics_names
for name, value in zip(metrics_names, final_results):
    print(f"  • {name}: {value:.4f}")