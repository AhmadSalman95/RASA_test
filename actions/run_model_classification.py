import tensorflow as tf
from tensorflow.keras import layers, losses
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import os

dir = os.path.dirname(os.path.realpath(__file__))
checkpoint_path = "{}/models_check_point/checkpointmodel/cp.ckpt".format(dir)
checkpoint_pathExportModel = "{}/checkpointExportModel/cp.ckpt".format(dir)

def ClassificationOfProblem(problem):
    problem = [problem]
    max_features = 50000
    sequence_length = 100
    class_name = ['Other',
                  'SIS',
                  'blackboard',
                  'helpdesk_support',
                  'learning_tech_resource',
                  'main_gate_university',
                  'maward',
                  'network_security',
                  'scientific_research_system',
                  'systems_infrastructure_apps',
                  'telephone_conferences',
                  'transaction_flow_system']

    def create_model():
        embedding_dim = 16
        model = tf.keras.Sequential([
            layers.Embedding(max_features + 1, embedding_dim),
            layers.Dropout(0.2),
            layers.GlobalAveragePooling1D(),
            layers.Dropout(0.2),
            layers.Dense(12, activation='softmax')])

        model.compile(loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                    optimizer='adam',
                    metrics=tf.metrics.SparseCategoricalAccuracy())
        return model


    model = create_model()
    model.load_weights(checkpoint_path)
    vectorize_layer = TextVectorization(max_tokens=max_features,
                                        output_mode='int',
                                        output_sequence_length=sequence_length)

    export_model = tf.keras.Sequential([
        vectorize_layer,
        model,
        layers.Activation('sigmoid')
    ])
    export_model.compile(
        loss=losses.SparseCategoricalCrossentropy(from_logits=False), optimizer="adam", metrics=['accuracy']
    )
    export_model.load_weights(checkpoint_pathExportModel)

    def get_string_labels(batch):
        predicted_int_labels = tf.argmax(batch, axis=1)
        predicted_labels = tf.gather(class_name, predicted_int_labels)
        return predicted_labels


    prediction = export_model.predict(problem)
    prediction_label = get_string_labels(prediction)
    for index, label in zip(problem, prediction_label):
        label = label.numpy()
        label = label.decode('utf-8')
    return label




# examples = [
#     "السلام عليكم عندي مشكلة في بلاك بورد المواد لا تظهر لي",
#     "السلام عليكم ورحمة الله وبركاته ارجو توصيل الانترنت على  غرفة الاجتماعات ",
#     "عندي المشكلة في موقع الجامعة لا استطيع ان دخول على صفحة نفاذ  "
# ]
# problem = "السلام عليكم عندي مشكلة في بلاك بورد المواد لا تظهر لي"

# label = ClassificationOfProblem(problem)
# print(label)