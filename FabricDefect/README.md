# 依赖环境
- **依赖安装编译**

   1. 创建并激活虚拟环境
        conda create -n pytorch python=3.7 -y
        conda activate pytorch

   2. 安装 pytorch
        conda install pytorch=1.1.0 torchvision=0.3.0 cudatoolkit=10.0 -c pytorch
        
   3. 安装其他依赖
        pip install cython && pip --no-cache-dir install -r requirements.txt
   
   4. 编译cuda op等：
        python setup.py develop

# 数据预处理
![Aaron Swartz](https://github.com/GitZWH-hub/DeepLearning/blob/master/FabricDefect/data_handle.png)

### 生成coco格式数据流程
1. copy老师给到的Febric_data文件夹到本项目FabricDefect目录下。
2. cd到train文件夹下，执行./train.sh脚本运行即可进行预处理，在data文件夹下生成instances_20211214.json文件。



