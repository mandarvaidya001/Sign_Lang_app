import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from augment import augment
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical

from config import (
    SEQUENCE_PATH,
    MODEL_PATH
)



from tensorflow.keras.layers import (
    Input,
    Bidirectional,
    LSTM,
    Dense,
    Dropout,
    BatchNormalization,
    Attention,
    LayerNormalization,
    GlobalAveragePooling1D
)

from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)

from tensorflow.keras.optimizers import Adam


# ==========================================
# LOAD DATASET
# ==========================================

X = []
y = []

print("\n=====================================")
print("Loading Normalized Landmark Dataset")
print("=====================================\n")


# ==========================================================
# DISCOVER ALL CLASSES
# ==========================================================

classes = set()


for category in sorted(os.listdir(SEQUENCE_PATH)):

    category_path = os.path.join(
        SEQUENCE_PATH,
        category
    )

    if not os.path.isdir(category_path):
        continue


    for cls in sorted(os.listdir(category_path)):

        class_path = os.path.join(
            category_path,
            cls
        )

        if not os.path.isdir(class_path):
            continue

        classes.add(cls)


# Convert set to sorted list
classes = sorted(classes)


print("Classes found:")
for i, cls in enumerate(classes):
    print(f"{i:2d} : {cls}")


# ==========================================================
# LOAD LANDMARK FILES
# ==========================================================

for category in sorted(os.listdir(SEQUENCE_PATH)):

    category_path = os.path.join(
        SEQUENCE_PATH,
        category
    )

    if not os.path.isdir(category_path):
        continue


    for cls in sorted(os.listdir(category_path)):

        class_path = os.path.join(
            category_path,
            cls
        )

        if not os.path.isdir(class_path):
            continue


        for file in sorted(os.listdir(class_path)):

            if not file.endswith(".npy"):
                continue


            file_path = os.path.join(
                class_path,
                file
            )


            try:

                data = np.load(file_path)


                # ------------------------------------------
                # Check expected shape
                # ------------------------------------------

                if data.shape != (30, 225):

                    print(
                        f"Skipping {file}: "
                        f"shape = {data.shape}"
                    )

                    continue


                # ------------------------------------------
                # Check invalid values
                # ------------------------------------------

                if not np.isfinite(data).all():

                    print(
                        f"Skipping {file}: "
                        "contains NaN/Inf"
                    )

                    continue


                X.append(data)

                y.append(cls)


            except Exception as e:

                print(
                    f"Error loading {file}: {e}"
                )


# ==========================================================
# CONVERT TO NUMPY
# ==========================================================

X = np.array(
    X,
    dtype=np.float32
)

y = np.array(y)


print()
print("Dataset Loaded Successfully!")
print(
    "Dataset Shape:",
    X.shape
)

print(
    "Labels Shape:",
    y.shape
)

print(
    "Number of Classes:",
    len(classes)
)

for cls in classes:

    class_path = os.path.join(
        SEQUENCE_PATH,
        cls
    )

    if not os.path.isdir(class_path):
        continue

    files = sorted(os.listdir(class_path))

    for file in files:

        if not file.endswith(".npy"):
            continue

        file_path = os.path.join(
            class_path,
            file
        )

        data = np.load(file_path)

        # ----------------------------------
        # Verify sequence shape
        # ----------------------------------

        if data.shape != (30, 225):

            print(
                f"Skipping {file} "
                f"because shape is {data.shape}"
            )

            continue

        X.append(data)
        y.append(cls)


print("Dataset Loaded Successfully!")

# ==========================================
# CONVERT TO NUMPY
# ==========================================

X = np.array(
    X,
    dtype=np.float32
)

print(
    "Dataset Shape:",
    X.shape
)

# Expected:
# (161, 30, 225)


# ==========================================
# LABEL ENCODING
# ==========================================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

num_classes = len(
    label_encoder.classes_
)

y = to_categorical(
    y,
    num_classes=num_classes
)

print(
    "Classes:",
    label_encoder.classes_
)

print(
    "Number of Classes:",
    num_classes
)


# ==========================================
# SAVE LABELS
# ==========================================

label_file = os.path.join(
    MODEL_PATH,
    "word_labels.npy"
)

np.save(
    label_file,
    label_encoder.classes_
)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    shuffle=True,

    stratify=np.argmax(
        y,
        axis=1
    )
)


# ==========================================
# TRAIN / VALIDATION SPLIT
# ==========================================

X_train, X_val, y_train, y_val = train_test_split(

    X_train,
    y_train,

    test_size=0.20,

    random_state=42,

    shuffle=True,

    stratify=np.argmax(
        y_train,
        axis=1
    )
)


# ==========================================
# DATA AUGMENTATION
# ==========================================

print("\n=====================================")
print("Applying Data Augmentation")
print("=====================================\n")

aug_X = []
aug_y = []

for i in range(len(X_train)):

    # --------------------------------------
    # Original sequence
    # --------------------------------------

    aug_X.append(
        X_train[i]
    )

    aug_y.append(
        y_train[i]
    )

    # --------------------------------------
    # Augmentation 1
    # --------------------------------------

    aug_X.append(
        augment(X_train[i])
    )

    aug_y.append(
        y_train[i]
    )

    # --------------------------------------
    # Augmentation 2
    # --------------------------------------

    aug_X.append(
        augment(X_train[i])
    )

    aug_y.append(
        y_train[i]
    )

    # --------------------------------------
    # Augmentation 3
    # --------------------------------------

    aug_X.append(
        augment(X_train[i])
    )

    aug_y.append(
        y_train[i]
    )


X_train = np.array(
    aug_X,
    dtype=np.float32
)

y_train = np.array(
    aug_y,
    dtype=np.float32
)


# ==========================================
# DATASET INFORMATION
# ==========================================

print("\n=====================================")
print("Dataset Information")
print("=====================================")

print(
    "Original Samples :",
    len(X)
)

print(
    "Classes           :",
    num_classes
)

print(
    "Train Samples     :",
    len(X_train)
)

print(
    "Validation Samples:",
    len(X_val)
)

print(
    "Test Samples      :",
    len(X_test)
)

print(
    "Train Shape       :",
    X_train.shape
)

print(
    "Validation Shape  :",
    X_val.shape
)

print(
    "Test Shape        :",
    X_test.shape
)

print(
    "Input Shape       :",
    X_train.shape[1:]
)


# ==========================================
# BUILD ATTENTION + BiLSTM MODEL
# ==========================================

print("\n=====================================")
print("Building Attention + BiLSTM Model")
print("=====================================\n")


# ==========================================
# ATTENTION + BiLSTM MODEL
# ==========================================

print("\n=====================================")
print("Building Attention + BiLSTM Model")
print("=====================================\n")


# ==========================================
# Input
# ==========================================

inputs = Input(
    shape=X_train.shape[1:]
)


# ==========================================
# BiLSTM Layer 1
# ==========================================

x = Bidirectional(
    LSTM(
        128,
        return_sequences=True
    )
)(inputs)

x = BatchNormalization()(x)

x = Dropout(0.30)(x)


# ==========================================
# SELF ATTENTION 1
# ==========================================

attention_1 = Attention()(
    [x, x]
)

x = LayerNormalization()(
    x + attention_1
)


# ==========================================
# BiLSTM Layer 2
# ==========================================

x = Bidirectional(
    LSTM(
        64,
        return_sequences=True
    )
)(x)

x = BatchNormalization()(x)

x = Dropout(0.30)(x)


# ==========================================
# SELF ATTENTION 2
# ==========================================

attention_2 = Attention()(
    [x, x]
)

x = LayerNormalization()(
    x + attention_2
)


# ==========================================
# Temporal Pooling
# ==========================================

x = GlobalAveragePooling1D()(x)


# ==========================================
# Dense Layer
# ==========================================

x = Dense(
    128,
    activation="relu"
)(x)

x = Dropout(0.40)(x)


# ==========================================
# Output
# ==========================================

outputs = Dense(
    num_classes,
    activation="softmax"
)(x)


# ==========================================
# Create Functional Model
# ==========================================

model = Model(
    inputs=inputs,
    outputs=outputs
)


# ==========================================
# Compile
# ==========================================

model.compile(

    optimizer=Adam(
        learning_rate=0.001
    ),

    loss="categorical_crossentropy",

    metrics=[
        "accuracy"
    ]
)


# ==========================================
# Summary
# ==========================================

model.summary()


# ==========================================
# COMPILE MODEL
# ==========================================

model.compile(

    optimizer=Adam(
        learning_rate=0.001
    ),

    loss="categorical_crossentropy",

    metrics=[
        "accuracy"
    ]

)


# ==========================================
# MODEL SUMMARY
# ==========================================

model.summary()


# ==========================================
# MODEL FILE
# ==========================================

MODEL_FILE = os.path.join(
    MODEL_PATH,
    "word_model_normalized_attention.keras"
)


# ==========================================
# CALLBACKS
# ==========================================

callbacks = [

    # --------------------------------------
    # Save best model
    # --------------------------------------

    ModelCheckpoint(

        MODEL_FILE,

        monitor="val_accuracy",

        save_best_only=True,

        verbose=1

    ),

    # --------------------------------------
    # Early stopping
    # --------------------------------------

    EarlyStopping(

        monitor="val_loss",

        patience=12,

        restore_best_weights=True,

        verbose=1

    ),

    # --------------------------------------
    # Reduce learning rate
    # --------------------------------------

    ReduceLROnPlateau(

        monitor="val_loss",

        factor=0.5,

        patience=5,

        min_lr=1e-6,

        verbose=1

    )

]


# ==========================================
# TRAIN MODEL
# ==========================================

print("\n=====================================")
print("Starting Training")
print("=====================================\n")


history = model.fit(

    X_train,

    y_train,

    validation_data=(
        X_val,
        y_val
    ),

    epochs=60,

    batch_size=8,

    callbacks=callbacks,

    verbose=1

)


# ==========================================
# FINAL TEST
# ==========================================

print("\n=====================================")
print("Evaluating Test Dataset")
print("=====================================\n")


loss, accuracy = model.evaluate(

    X_test,

    y_test,

    verbose=1

)


# ==========================================
# FINAL RESULT
# ==========================================

print("\n==============================")
print("Final Test Accuracy")
print("==============================")

print(
    f"Loss     : {loss:.4f}"
)

print(
    f"Accuracy : {accuracy * 100:.2f}%"
)


print("\n=====================================")
print("Model Saved")
print("=====================================")

print(
    MODEL_FILE
)