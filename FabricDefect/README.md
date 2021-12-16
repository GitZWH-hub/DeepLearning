# 依赖环境
- **依赖安装编译**

   1. 创建并激活虚拟环境
        conda create -n guangdong python=3.7 -y
        conda activate guangdong

   2. 安装 pytorch
        conda install pytorch=1.1.0 torchvision=0.3.0 cudatoolkit=10.0 -c pytorch
        
   3. 安装其他依赖
        pip install cython && pip --no-cache-dir install -r requirements.txt
   
   4. 编译cuda op等：
        python setup.py develop

# 数据预处理
![Aaron Swartz](https://github.com/GitZWH-hub/DeepLearning/blob/master/FabricDefect/data_handle.png)





