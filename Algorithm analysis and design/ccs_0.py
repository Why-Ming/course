import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score

# 加载鸢尾花数据集
iris = load_iris()
X, y = iris.data, iris.target

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定义超参数搜索空间
search_space = {
    'n_estimators': np.arange(10, 101, 10),
    'max_depth': np.arange(2, 11),
    'min_samples_split': np.arange(2, 11),
    'min_samples_leaf': np.arange(1, 11)
}

# 定义麻雀搜索算法
def sparrow_search(search_space, iterations):
    best_params = None
    best_accuracy = 0.0
    
    # 记录每次迭代的超参数、性能和预测结果
    history_params = []
    history_accuracy = []
    history_predictions = []
    
    for _ in range(iterations):
        # 改变随机种子
        current_params = {param: np.random.choice(values) for param, values in search_space.items()}
        model = RandomForestClassifier(**current_params, random_state=np.random.randint(100))
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # 将预测结果四舍五入为整数
        y_pred_discrete = np.round(y_pred).astype(int)
        
        # 计算平衡准确度
        current_accuracy = balanced_accuracy_score(y_test, y_pred_discrete)
        
        # 记录数据
        history_params.append(current_params)
        history_accuracy.append(current_accuracy)
        history_predictions.append(y_pred_discrete)
        
        if current_accuracy > best_accuracy:
            best_params = current_params
            best_accuracy = current_accuracy
    
    # 返回最佳超参数、整个搜索过程中的数据和最佳模型的预测结果
    return best_params, history_params, history_accuracy, history_predictions

# 运行麻雀搜索算法
best_hyperparameters, params_history, accuracy_history, predictions_history = sparrow_search(search_space, iterations=50)

# 打印最佳超参数
print("最佳超参数：", best_hyperparameters)

# 绘制超参数搜索过程的数据变化图
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
axs = axs.flatten()

param_names = list(search_space.keys())

for i in range(4):
    param_values = [params[param_names[i]] for params in params_history]
    axs[i].plot(param_values, accuracy_history, 'o-', label=f'{param_names[i]} vs. Accuracy')
    axs[i].set_xlabel(param_names[i])
    axs[i].set_ylabel('Balanced Accuracy')
    axs[i].legend()

plt.tight_layout()
plt.show()

# 展示每次迭代后的模型预测结果
fig, axs = plt.subplots(5, 10, figsize=(20, 10))
axs = axs.flatten()

for i in range(len(predictions_history)):
    axs[i].scatter(X_test[:, 0], X_test[:, 1], c=predictions_history[i], cmap='viridis')
    axs[i].set_title(f'Iteration {i + 1}')
    axs[i].set_xticks(())
    axs[i].set_yticks(())

plt.tight_layout()
plt.show()
