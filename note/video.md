## 基于FFmpeg的解码流程

FFmpeg可以直接作为命令行使用

1、基于ACodec API

    1、查找解码器
        avcodec_find_decoder
        用于解析不同种类的视频，如mp4、h264
    2、分配解码环境
        avcodec_alloc_context3
        用于存储解码过程和一些参数
    3、打开解码器​​
        avcodec_open2
        解码器需要单独打开，与context上下文是两个东西
    4、循环解码
        过程异步，因此需要多次发送或者接收帧才能得到一个帧
        1）读取数据包
            av_read_frame
            读取一个压缩包AVPacket
        2）​​发送数据包
            avcodec_send_packet 
            将压缩包发送给解码器内部队列
        3）接收帧
            avcodec_receive_frame 
            从解码器队列中获取解码完成的原始AVFrame

2、硬件加速

    FFmpeg可以指定特殊的解码器来实现GPU硬件加速

3、视频压缩

    即编码，常用格式如下：
        ​​H.264​​： libx264（最流行、最均衡的编码器）
        ​​H.265/HEVC​​： libx265（比H.264压缩率更高，但更慢）
        ​​AV1​​： libaom-av1（新一代 royalty-free 编码格式，压缩率极高，但编码速度非常慢）
        ​​VP9​​： libvpx-vp9（Google开发的 royalty-free 格式，是AV1的前身）

    还可以使用硬件编码，常用于直播推流、实时录制，快但质量低

    编码参数：
    
        ​​恒定质量模式（CRF）​​： -crf <数值>。数值越小，质量越高，文件越大。这是最常用的离线制作模式。（x264的CRF范围是0-51，默认23）
        ​​平均比特率（ABR）​​： -b:v 2000k。设定一个目标平均码率，控制简单但效率不高。
        ​​二次编码（2-Pass）​​： 先分析整个视频（第一遍），再根据分析结果进行编码（第二遍）。可以在指定目标文件大小（-fs）或目标平均码率时获得最佳的质量和压缩比。
        ​​预设（Preset）​​： -preset slow|medium|fast。控制编码速度和压缩效率的权衡。越慢的预设，压缩率越高（同质量下文件更小）。

4、视频处理

    编码与容器
    1）编码格式（Codec）
        决定视频数据如何被压缩（编码）和还原（解码）
        ​纯数据层面
    2）容器格式（Container）​
        封装多个媒体流（如视频流、音频流、字幕流）
        提供同步播放的元数据（如时间戳、章节信息）
        支持随机访问（如快速跳转到指定时间点）
        不同容器对编码格式的支持不同（例如AVI不支持H.265，MP4不支持VP9

    转码
        即改变视频的编码格式或参数
    改变封装格式
        将mp4改成avi
    视频分析过滤
        提取某一帧、添加水印、裁剪旋转等
    流式传输
        将视频以流式方式传输到流媒体服务器
        ffmpeg -re -i input.mp4 -c:v libx264 -preset veryfast -f flv rtmp://live.twitch.tv/app/your-stream-key

5、帧跳转

    FFmpeg命令行中可以通过-ss来指定跳转的位置，与-i先后不同，导致的结果也不同
        先使用即先找到距离指定时间最近的关键帧，速度很快
        后使用即先解码全部然后直接跳到指定时间，速度很慢

    在C代码中执行跳转需要使用到av_seek_frame
        flags: 
            AVSEEK_FLAG_BACKWARD 
                表示向后搜寻到最近的关键帧
            AVSEEK_FLAG_ANY      
            可以seek到任何帧，包括非关键帧（但可能无法解码）
        在这之后再使用read_frame，得到的包就是seek位置附近的
