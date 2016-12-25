# sEMG-classification-tool
为肌电信号的处理、特征提取和绘图工具。tools包中为读取txt文件、提取特征以及绘图的工具，均封装成类。

## 依赖：
- python2.7
- numpy: 下载(http://www.lfd.uci.edu/~gohlke/pythonlibs/) 安装 pip install 文件名.whl
- matplotlib：pip install matplotlib
- pandas: pip install pandas
- seaborn: pip install seaborn

## API Reference:

介绍此工具的使用方法。

### 1. tools.reader

#### FilesReader 读取txt数据文件，规定数据文件以数字排序命名。

**class tools.reader.FilesReader（columns, path）**

**parameters:**

*columns*: int  数据文件的列数

*path*: string  数据文件所在路径

**Attributes:**

*fileList*: list  path下文件列表

*fileNumber*: int path下文件的数量

*filesLength*: tuple 已导入文件的各自行数

*_nameSortMethod*: lambda function  文件名排序规则，决定导入文件的顺序，默认文件名为数字序号，按数字序号排序

**Method:**

*files*: 返回path目录下的文件，返回类型list(string,string,...)

*allFilesData*: 导入并返回路径下所有文件的数据，返回类型list(numpyArray,numpyArray,...)，文件按_nameSortMethod进行排序。

*loadFile(fileName)*: 输入String类型文件名，导入文件数据，并返回数据矩阵，返回类型numpyArray


### 2. tools.featureExtrac

#### FeatureExtractor 特征提取工具，包括RMS，ZC，3-order ARC的提取：

**class tools.featureExtrac.featureExtractor（gestNumber, gestSize, winSize, featRavel = True）**




