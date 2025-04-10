import os
import requests
import logging

from Algorithm.AlgorithmImplement import AlgorithmImplement
from Framework.AlgorithmSystemManager import AlgorithmSystemManager
from Task.TaskManager import TaskManager
from TestData.loadData import ImageCollector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestFace")

if __name__ == '__main__':
    algorithmSystemManager = AlgorithmSystemManager()

    # 生成TaskManager的实例
    taskManager = TaskManager()
    # 注入框架
    algorithmSystemManager.addTask(taskManager)

    # 加载图像数据
    # dataPath = os.path.join(os.getcwd(), 'TestData')
    dataPath = '/app/app/TestData'
    ImagedataPath = os.path.join(dataPath, 'Faces_test')

    ImageCollector = ImageCollector(ImagedataPath)
    images, labels = ImageCollector.load_data()

    # 注入图像数据
    algorithmSystemManager.addData(images, labels)
    # 生成算法实例
    algorithmImplement = AlgorithmImplement()
    # 注入算法
    algorithmSystemManager.addAlgorithm(algorithmImplement)
    # 执行算法
    algorithmSystemManager.run()
    # 获取评分
    scoreModel = algorithmSystemManager.getScore()
    # 输出结果
    score = scoreModel.score
    print(f"最终得分：{score}")
    logger.info(f"[SUCCESS]最终得分:{score}")

    # get env
    task_id = os.environ.get("TASK_ID")
    logger.info(f"taskID:{task_id}")

    # get score URL
   # 获取更新分数的URL
    update_score_url = None

    # 遍历环境变量查找URL
    for env_var in os.environ.values():
        if "URL=" in env_var:
            update_score_url = env_var.split("URL=", 1)[1]
            break

    # 如果没有找到环境变量，使用默认值
    if not update_score_url:
        update_score_url = "http://10.101.165.60:88/task/updateScore"

    logger.info(f"更新分数URL: {update_score_url}")

    # 发送分数到后端
    try:
        # 构建请求URL
        request_url = f"{update_score_url}?taskId={task_id}&score={score}"
        logger.info(f"发送请求: {request_url}")

        # 发送请求
        response = requests.post(request_url)

        # 记录响应
        logger.info(f"分数更新响应: {response.status_code} - {response.text}")

        if response.status_code == 200:
            logger.info("分数更新成功!")
        else:
            logger.error(f"分数更新失败，状态码: {response.status_code}")
    except Exception as e:
        logger.error(f"分数更新异常: {str(e)}")

        # 清除算法
    algorithmSystemManager.clearAlgorithm()
    # 清除数据
    algorithmSystemManager.clearData()
    # 清除赛题
    algorithmSystemManager.clearTask()