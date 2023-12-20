import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

# 加载MNIST数据集
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# 定义神经网络层数搜索空间
search_space = {
    'num_layers': np.arange(1, 6),
    'num_neurons': np.arange(16, 256, 16),
    'learning_rate': [0.001, 0.01, 0.1]
}

# 定义麻雀搜索算法
def sparrow_search(search_space, iterations):
    best_params = None
    best_accuracy = 0.0
    
    # 记录每次迭代的层数和性能
    history_layers = []
    history_accuracy = []
    
    for _ in range(iterations):
        current_params = {param: np.random.choice(values) for param, values in search_space.items()}
        
        # 记录当前的层数
        current_layers = current_params['num_layers']
        history_layers.append(current_layers)
        
        model = Sequential()
        model.add(Flatten(input_shape=(28, 28)))
        
        for _ in range(current_layers):
            model.add(Dense(current_params['num_neurons'], activation='relu'))
        
        model.add(Dense(10, activation='softmax'))
        
        optimizer = Adam(learning_rate=current_params['learning_rate'])
        model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        
        model.fit(x_train, y_train, epochs=5, verbose=0, validation_split=0.2)
        _, current_accuracy = model.evaluate(x_test, y_test, verbose=0)
        
        # 记录性能
        history_accuracy.append(current_accuracy)
        
        if current_accuracy > best_accuracy:
            best_params = current_params
            best_accuracy = current_accuracy
            
    return best_params, history_layers, history_accuracy

# 运行麻雀搜索算法
best_hyperparameters, layers_history, accuracy_history = sparrow_search(search_space, iterations=50)

# 打印最佳超参数
print("最佳超参数：", best_hyperparameters)

# 绘制神经网络层数搜索过程的数据变化图
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Accuracy', color=color)
ax1.plot(accuracy_history, label='Validation Accuracy', marker='o', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Number of Layers', color=color)
ax2.plot(layers_history, label='Number of Layers', marker='x', linestyle='--', color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Neural Network Layers Search Process')
plt.show()