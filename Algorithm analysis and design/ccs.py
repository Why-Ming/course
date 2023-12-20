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
    
    # 记录每次迭代的超参数和性能
    history_params = []
    history_accuracy = []
    
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
        
        if current_accuracy > best_accuracy:
            best_params = current_params
            best_accuracy = current_accuracy
            
    return best_params, history_params, history_accuracy

# 运行麻雀搜索算法
best_hyperparameters, params_history, accuracy_history = sparrow_search(search_space, iterations=50)

# 打印最佳超参数
print("最佳超参数：", best_hyperparameters)

# 绘制超参数搜索过程的数据变化图
fig, ax = plt.subplots(figsize=(10, 6))
for i, acc in enumerate(accuracy_history):
    ax.scatter([i], acc, label=f'Iteration {i+1}', marker='o', alpha=0.5)

ax.set_xlabel('Iterations')
ax.set_ylabel('Balanced Accuracy')
ax.set_title('Hyperparameter Search Process')
#ax.legend()
plt.show()
