## Stable Diffusion 须知

1、Text Encoder

    通常指Clip，将指定提示词Prompt翻译成模型语言（一串数值向量）
    Clip模型作用是将文字与图像概念在语义空间对齐

2、U-Net

    Latent Space潜在空间，即一个充满随机噪声的变量，U-Net噪声预测器，通过正负向提示词预测出去噪的部分，设置step多次迭代

3、VAE

    Encoder，分解图片成更小的单位
    Decoder，还原潜变量为图像

    