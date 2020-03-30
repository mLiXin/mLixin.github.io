---
title: 深入理解Android:Java虚拟机ART 学习笔记
date: 2019-5-09 14:39:43
tags:
- Android
- 虚拟机
- ART
categories:
- Android
---
#### 摘要
暂时大概了解，深入太难，等我哪天C++写溜了再来。Done for now.

#### 第2章 深入理解Class文件格式
0. 扩展阅读
    - [Java vm官方规范](https://docs.oracle.com/javase/specs/jvms/se7/html/index.html)
        - Class文件格式在第4章
        - Java指令码的内容在第6、7章
1. Class文件是什么？
    - Java源代码经Java编译器编译后得到的Java字节码文件，可以看做是Java虚拟机的可执行文件。

2. Class文件
    1. u4:magic
        - 取值必须是0xCAFEBABE
    2. u2:minor_version
        - class文件版本的小版本信息
    3. u2:major_version
        - class文件版本的大版本信息
    4. u2:constant_pool_count
        - 常量池数组中元素的个数
    5. cp_info:constant_pool[constant_pool_count-1]
        - 大小为constant_pool_count决定，是一个存储cp_info信息的数组。每个Class文件都包含一个常量池。常量池在代码中对应为一个数组，数组元素类型就是cp_info。注意数组索引从1开始。
    6. u2:access_flags
        - 表明该类的访问权限，public、private之类
    7. u2:this_class
        - 存储的是指向常量池数组元素的索引，通过这个索引和常量池对应元素的内容，可以知道本类的类名(只是类名，不包含包名，类名最终用字符串描述)
    8. u2:super_class
        - 存储的是指向常量池数组元素的索引，通过这个索引和常量池对应元素的内容，可以知道父类的类名(只是类名，不包含包名，类名最终用字符串描述)
    9. u2:interfaces_count
        - 存储的是指向常量池数组里的索引，通过这个索引可以知道该类实现了多少个接口
    10. u2:interface[interfaces_count]
        - 存储的是指向常量池数组里的索引，通过这个索引可以知道接口类的类名
    11. u2:fields_count
        - 成员变量的数量
    12. field_info:fields[fields_count]
        - 成员变量的信息
    13. u2:methods_count
        - 成员函数的数量
    14. method_info:methods[methods_count]
        - 成员函数的信息
    15. u2:attributes_count
        - 属性信息数量
    16. attribute_info:attributes[attributes_Count]
        - 属性信息(调试信息就记录了某局代码对应源文件哪一行、函数对应的Java字节码也属于属性信息的一种。另外源文件中的注解也属于属性。)

3. 常量池及相关内容
    - 常量池对应的就是一个类型为cp_info的数组，每一个cp_info存储了一个常量项，每一个常量项的第一个字节用于表明常量项的类型，后面才是具体的常量项内容。
        - 具体常量类型可见章节底部表格。
4. 为什么要单独分一个CONSTANT_UTF8类型出来存储字符串？
    - CONSTANT_Class/Fieldref/String/Method/Methodref等等最后包含的内容都是字符串，这样可以节省Class文件的空间。
    - Android的dex文件在 Class文件基础上做了进一步的优化以节省空间。
5. 如何用字符串来描述成员变量、成员函数？
    - 数据类型的描述规则
        - 原始数据类型B/C/D/F/I/J/S/Z分别对应byte/char/double/float/int/long/short/boolean
        - 引用数据类型`LClassName`(ClassName为对应类的全路径名 ),如`Ljava/lang/String`，表示String类型
        - 数组也是引用类型，用`[其他类型的描述名`来表示，如int数组表示为`[I`,字符串数组表示为`[java/lang/String`，二维数组表示为`[[I`
    - 成员变量的描述规则(Field Descriptor)
        - FieldDescriptor：只包含FieldType一种信息
        - FieldType：
            - BaseType：B|C|D|F|I|J|S|Z
            - ObjectType: L ClassName
            - ArrayType:[ ComponentType(ComponentType由上面的FieldType构成)
    - 成员函数的描述规则(Method Descriptor)
        - MethodDescriptor的描述需要包含返回值及参数的数据类型
        - MethodDescriptor
        - ParamterDescriptor：FieldType
        - ReturnDescriptor：Field|VoidDescriptor
        - 举例
            - `System.out.println(String str)`对应Method Descriptor为`(Ljava/lang/String；)V`

6. acess_flags介绍
    - Class的特殊access_flags取值
        - ACC_SUPER：用于invokespecial指令
        - ACC_SYNTHETIC：表明该类由编译器根据情况生成，源码里无法显示定义这样的类。
    - Field的access_flag取值
        - ACC_TRANSIENT：说明该成员不能被串行化
        - ACC_SYNTHETIC：说明该成员由编译器根据情况生成的，源码里无法显示定义这样的成员
    - Method的access_flag
        - ACC_SYNCHRONIZED：synchronized函数
        - ACC_BRIDGE：桥接方法，由编译器根据情况生成
        - ACC_VARARGS：可变参数个数的函数
        - ACC_STRICT：strictfp函数(strict float point,精确浮点)
        - ACC_SYNTHETIC：表明该成员由编译器根据情况生成的，源码里无法直接定义这样的成员。
7. 属性包括哪些？
    - attribute_name_index:属性名称，指向常量池UTF8常量项的索引
        - ConstantValue：fieldInfo中出现，描述一个常量成员域
        - Code：methodInfo中出现，用于描述一个函数的内容，即源码中该函数内容编译后得到的虚拟机指令
        - Exceptions：一个函数抛出异常或错误，methodInfo中会有此属性
        - SourceFile：包含一个指向utf8常量项的树荫，包含此Class对应的源码文件名
        - LocalVariableTable：属性还可以包含属性，改属性就是包含在Code属性中的，用来描述一个函数的本地变量相关信息，比如这个变量的名字，这个变量在源码哪一行定义的。
    - attribute_length：该属性具体内容的长度，即下面info数组的长度
    - info[attribute_length]：属性具体内容
8. code属性都包括哪些内容？
    - 函数的内容(这个函数的源码转换后得到的Java字节码)就存储在Code属性中。
    - 主要包括：
        - attribute_name_index：指向内容为"code"的utf8_info常量项
        - max_stack、max_locals：JVM执行指令的时候，操作数存储在操作数栈中，没一个操作数占用一个或者两个栈顶。max_stack说明这个函数在执行过程中，需要最深多少栈空间。max_locals表示该函数包括最多几个局部变量
        - code_length和code：函数对应的指令内容也就是这个函数的源码经过编译器转换后得到的Java指令码存储在code数组中，长度由code_length表明
        - exception_table_length和exception_table：一个函数可以包含多个try/catch语句，一个try/catch语句对应exception_table数组中的一项。
            - 包括stact_pc、end_pc、handler_pc、cache_type
9. LineNumberTable属性包括哪些内容？
    - 用于Java的调试，可指明某条指令对应于源码哪一行。
    - 主要包括：
        - start_pc：指向Code_attribute中code数组某处指令
        - line_number：说明start_pc位于源码的哪一行
10. LocalVariableTable属性包括哪些内容？
    - 用于描述一个函数具备变量相关的信息
    - 主要包括：
        - start_pc和length：局部变量在code数组中的有效范围
        - name_index：局部变量的名字
        - descriptor_index：局部变量的类型
11. Java指令码介绍(了解即可)
    - Java指令码长度为一个字节，指令码后面跟0或多个参数
        - JVM规范第6章：介绍每个指令码的格式、所带参数、功能及使用场景
        - JVM规范第7张：指令码的取值和对应的助记符
    - 指令码
        - invokevirtual指令
        - dup_x1指令：栈顶v1、v2，使用这个指令以后，编程栈顶v1、v2、v1 

| 常量项类型 | tag取值    | 含义 |
| -------- | ------------|-----|
|CONSTANT_Class|7|代表类或接口的信息|
|CONSTANT_Fieldref |9|成员变量信息，包括所属类的类名、变量和函数名、函数参数、返回值类型等。|
|CONSTANT_Methodref|10|成员函数信息，包括所属类的类名、变量和函数名、函数参数、返回值类型等。|
|CONSTANT_InterfaceMethodref|11|接口函数信息，包括所属类的类名、变量和函数名、函数参数、返回值类型等。|
|CONSTANT_String|8|代表一个字符串，本身不存储字符串的内容，只存储一个索引值|
|CONSTANT_Integer|3|4个字节，int型数据的信息|
|CONSTANT_Float|4|4个字节，float型数据的信息|
|CONSTANT_Long|5|8个字节，long型数据的信息|
|CONSTANT_Double|6|8个字节，double型数据的信息|
|CONSTANT_NameAndType|12|描述类的成员域或成员函数相关的信息|
|CONSTANT_Utf8|1|存储字符串的常量项，真正包含了字符串的内容。CONSTANT_String只存储了一个指向这里的索引|
|CONSTANT_MethodHandle|15|描述MethodHandle信息，MethodHandle和反射有关系|
|CONSTANT_MethodType|16|描述一个成员函数的信息，只包括函数的参数类型和返回值类型，不包含函数名和所属类的类名|
|CONSTANT_InvokeDynamic|18|用于invokeDynamic指令。invokeDynamic和Java平台上实现了一些动态语言相类似的有关功能|

#### 第3章 深入理解Dex文件格式
1. 为什么不直接使用Class文件，而用Dex？
    - Dex核心内容和Class文件类似，可以和Class文件相互转化，但是Android虚拟机只能识别Dex文件
    - 移动设备内存、存储空间小，主要使用ARM的CPU，通用寄存器较多。

2. Dex和Class文件格式的区别？
    - 字节码文件的创建
        - 一个Class文件对应一个Java源码文件，而一个Dex文件可对应多个Java源码文件。
        - Android里面的Java源文件会先编译成多个.class文件，然后再合并到classes.dex文件中
            - class文件之间存在重复字符串等信息，而classes.dex由于包含了多个Class文件的内容，可以进一步去除其中的重复信息。
            - 如果一个class文件依赖另一个class文件，则虚拟机处理的时候，需要读取另外一个class文件的内容，这可能导致CPU和存储设备进行更多的I/O操作，而classes.dex由于一个文件就包含了所有的信息，相对而言会减少I/O操作的次数
    - 字节序
        - Java平台字节序是Big Endian，所以class文件也是采用的Big Endian字节序来组织内容的。而Android平台上的Dex文件默认的字节序是Little Endian
            - 大端字节序（big endian）：高位字节在前，低位字节在后，这是人类读写数值的方法。
            - 小端字节序（little endian）：低位字节在前，高位字节在后，即以0x1122形式储存。
    - 新增LEB128数据类型
        - Dex文件定义了一种名为LEB128的数据类型(Little Endian Based 128),唯一的功能就是用于表示32位比特位长度的数据。
    - 信息描述规则
        - 数据类型描述没有区别 
        - 简短描述
            - Dex文件格式中，简短描述用来描述函数的参数和返回值信息，类似Class文件格式的MEthodDescriptor，不过省略了很多字符。

3. Dex文件都包括哪些内容？
    - 概括来说：header_item(header)、string_ids、type_ids(类型相关)、proto_ids、field_ids(成员变量)、method_ids(成员函数)、class_defs(类的信息)、data(重要的数据内容)、link_data(预留区域)
    - header_item
        - Dex文件头结构的类型，主要包括
            - magic：取值固定
            - checksum：文件内容的校验和，不包括magic和自己，用于检查文件是否损坏
            - signature：签名信息，不包括magic、checksum和自己，用于检查文件是否被篡改
            - file_size：整个文件的长度
            - header_size：默认是0x70个字节
            - endian_tag：表示文件内容应该按什么字节序来处理，默认Little Endian
    - xxx_id_item(xxx_ids)
        - string_id_item
        - type_id_item
        - proto_id_item
        - field_id_item
        - method_id_item
    - class_def
    - code_item 

4. Dex指令码和Java指令码的区别？
    - Dex文件中存储函数内容的insns数组比Class文件中存储函数内容的code数组解析起来要有难度。
        - Andorid虚拟机在执行指令码的时候不需要操作数栈，所有参数要么和Class指令码一样直接跟在指令码后面，要么就存储在寄存器中。这样指令码就需要携带一些信息来表示该指令执行的时候需要操作哪些寄存器。

#### 第4章 深入理解ELF文件格式
0. 了解即可，应用层面不用理解太多。
1. Java虚拟机的可执行文件是.class文件，Dalvik虚拟机的可执行文件是.dex文件，而ART虚拟机的可执行文件是.oat文件
2. .oat是一种定制化的ELF文件，所以ELF文件是oat文件的基础。
3. ELF文件的两个特性？
    - Executable：可执行。ELF文件将参与程序的执行工作。包括二进制程序的运行以及动态库.so文件的加载
    - Linkable：可链接。ELF文件是编译链接工作的重要参与者
4. ELF文件包括哪些内容？
    - 头结构
    - Linking View：链接视图，从编译链接的角度来观察一个ELF文件应该包含哪些内容
    - Execution View：执行视图，从执行的角度来观察一个ELF文件应该包含什么信息

#### 第14章 ART中的GC
1. Mark-Sweep Collection原理
    - Mark阶段：搜索内存中的Java对象(对ART虚拟机而言，就是从root set遍历Object对象)，对那些能搜到的对象进行标记
    - Sweep阶段：释放那些没有被标记的对象所占据的内存。

2. Copying Collection原理
    - 将堆分为大小相同的两个空间，fromspace、tospace。对象的内存分配只使用tospace
    - tospace空间不够用的时候将触发GC。GC的第一个工作就是将指向这两个空间的变量进行互换
    - 从root set开始遍历，将遍历过程中访问到的对象从fromspace拷贝到tospace中。
    - 当fromspace中活对象全部拷贝完后，该空间的内存就可以整体释放。
    - tips：还有另外一种Copying的实现方式，是分了三块内存去处理

3. Mark-Compact Collection原理
    - Mark阶段，从root set触发遍历对象以标记存活的对象，没有被标记的则认为是垃圾对象
    - 压缩阶段，将存活对象挪到一起去。

4. 其他的重要概念
    - mutator和collector
        - collector表示内存回收相关的功能模块，mutator代表应用程序中除collector之外的其他部分
    - Incremental Collection(增量回收)
        - 分代GC是增量回收的一种实现方式，heap被划分为新生代、老年代等部分，而GC往往只针对其中某一代，符合增量式回收的定义。
        - 早期GC实现中，垃圾回收会扫描全部的堆内存，需要暂停所有其他非GC线程的运行才能执行一次GC，对程序运行的影响非常大，而增量式回收可以每次只针对heap的一部分做GC，从而大幅度减少停顿时间。
    - Parallel Collection(并行回收)
        - 程序中有多个垃圾回收线程，它们可以同时执行回收工作中的某些任务。比如Mark-Sweep算法而言，可以使用多个线程来做标记工作。
    - Concurrent Collection(并发回收)
        - 程序中垃圾回收线程虽然只有一个，但是在回收工作的某个阶段，回收线程可以和其他非回收线程(mutator)同时运行，这样对程序运行的影响更小。相反，不适用concurrent collection的话，回收线程在工作的时候可能就需要暂停mutator线程的执行，也就是stop-the-world的情况，对程序影响较大。

5. 通过Runtime VisitRoots函数可知，root set包含的内容大致可从下面几个方面获取？(不是通过其他Object对象的引用型成员来找到的，而只能由虚拟机根据其实现的特点来确定)
    - 每一个Thread对象的VisitRoots函数
    - JavaVmExt的VisitRoots
    - Runtime成员变量sentinel、pre_allocated_OutOfMemoryError_和pre_allocated_NoClassDefFoundError_。这三个变量代表Java层的三个对象，由虚拟机直接持有，所以它们对应的root类型为kRootVMInternal
    - RegTypeCache VisitStaticRoots函数
    - InternTable VisitRoots函数
    - ClassLinker VisitRoots函数
    - Runtime VisitConstantRoots函数
