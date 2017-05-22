# sEMG-classification-tool
为肌电信号的处理、特征提取和绘图所写的工具。tools中的内容为该工具，包括批量读取txt文件、提取特征以及绘图的工具，均封装成类。

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

**parameter:**

*gestNumber*: int 手势种类数

*gestSize*: int 每个手势的数据长度

*winSize*: int 特征窗的数据长度

*featRavel*: bool 标志着在计算各个特征时，是否对特征矩阵进行拉直展平，默认Ture，即允许特征拉直。在构造特征样本已进行分类时，需要进行展平，使每个样本对应一行数据。但是，在需要绘制特征图时，展平会破坏特征之间的对应关系，因此此时需要设置为False，禁止展平

**Method:**

*segmentation(data, index, ravel = False)*: 对原始数据矩阵进行分段，每段的数据将作为一个手势样本，返回分段后的列表，列表每个元素对应一段数据矩阵; data: 输入数据 numpyArray; index: 手势类别(第几个文件); ravel: 分段的时候是否进行展平, bool, 默认False

*_RMS*, *_ZC*, *_ARC3(data)*: 用于特征计算的子函数，输入为每窗的数据，进行一次相应运算，返回特征向量，向量中每个元素对应每通道的特征值

*RMSfeat(segData)*: 用于计算RMS特征的函数，输入为分段后的一段数据，当featRavel=Ture时输出展平后的特征，其为一个向量，而当featRavel=False时返回未展平的特征，为一个特征矩阵

*ZCfeat(segData)*: 计算ZC特征的函数，用法同上

*ARCfeat(segData, strack = True)*: 计算ARC特征的函数，strack = True 时arc各个系数对应特征会合并存储，返回numpyArray。否则会分别存储在列表中，返回以每个系数特征矩阵为元素的列表

*creatLabels(classIndex, length)*: 为已知类别样本创建标签，输入classIndex为类别，length为该类别的样本数量

*dynamicSplice(mat, dynamicMat, index, axis = 0)*: 在一次特征循环提取中对特征矩阵进行动态拼接，mat为 要生成的矩阵，需要初始化为np.array([]); dynamicMat为每次循环的更新项，index为循环的当前索引。 该函数可以动态的将每次循环计算得到的dynamicMat 拼接至mat中，axis 为拼接方向，0为纵向，1为横向

*creatFeatName(nameList,channels)*: 为生成的特征样本进行构造命名，namelist: 特征名列表; channels: 通道名列表


### 3. tools.Myplot
#### DataPlotter 针对信号特征分析的绘图类，基于pandas数据结构，以及matplotlib和seaborn绘图工具包：

**class tools.Myplot.DataPlotter（data, columns, subNum = -1）**

**Parameter:**

*data*: numpyArray 要绘制的数据，将以列为区分绘图，每列为同一个特征的数据

*columns*: [string,string,...] 数据的命名

*subNum*: 如果使用subplot需填写subplot的标志数字如431代表按4行3列进行分图，不填默认为-1，即不进行subplot

**Method:**

*plot(selectcol, xylabel=[], ls='-', lw=1 )*: 绘制单个图，selectol为要绘制的数据名组成的列表; xylabel为x和y坐标轴名字,默认无，格式为['X_name',u'Y—名字], 注意用到中文是字符串应为Unicode形，即前面应加上u; ls为线形，默认实线，可以设置selectcol中对应位置的数据的线形，以列表形式输入; lw为线的粗细，默认1，用法同ls

*legend()*: 对绘制的图添加图例

*subplot(number, selectcol, xylabel = [],ls='-',lw=1 )*: 绘制分图，
*number*: matpltlib中subplot的当前分图标志数，可以输入int如：431，也可输入list如[4,3,1], 表示绘制4行3列的分图，目前绘制第一个;  selectcol,xylabel,ls,lw的用法同plot

*newSubplot(self,number,data,color = 0, label = '', xylabel = [],ls='-',lw=1)*:绘制含有新数据的分图，当需要在某个子图中绘制类对象中未存储的数据时是可用。
