import torch as th
import torch.nn.functional as F


class UNetDiscriminatorSN(th.nn.Module):
    """U-Net discriminator with spectral normalization.
    Adapted from Real-ESRGAN [Wang 2021]
    """

    def __init__(
        self, input_dim: int = 3, channels_dim: int = 64, skip_connection: bool = True
    ):
        super().__init__()
        self.skip_connection = skip_connection
        norm = th.nn.utils.spectral_norm

        self.conv0 = th.nn.Conv2d(input_dim, channels_dim, kernel_size=3, stride=1, padding=1)

        self.conv1 = norm(th.nn.Conv2d(channels_dim, channels_dim * 2, 4, 2, 1, bias=False))
        self.conv2 = norm(th.nn.Conv2d(channels_dim * 2, channels_dim * 4, 4, 2, 1, bias=False))
        self.conv3 = norm(th.nn.Conv2d(channels_dim * 4, channels_dim * 8, 4, 2, 1, bias=False))
        # upsample
        self.conv4 = norm(th.nn.Conv2d(channels_dim * 8, channels_dim * 4, 3, 1, 1, bias=False))
        self.conv5 = norm(th.nn.Conv2d(channels_dim * 4, channels_dim * 2, 3, 1, 1, bias=False))
        self.conv6 = norm(th.nn.Conv2d(channels_dim * 2, channels_dim, 3, 1, 1, bias=False))

        # extra
        self.conv7 = norm(th.nn.Conv2d(channels_dim, channels_dim, 3, 1, 1, bias=False))
        self.conv8 = norm(th.nn.Conv2d(channels_dim, channels_dim, 3, 1, 1, bias=False))

        self.conv9 = th.nn.Conv2d(channels_dim, 1, 3, 1, 1)

    def forward(self, x):
        x = x.contiguous()  # fixes an issue when x is generated by a unet
        x0 = F.leaky_relu(self.conv0(x), negative_slope=0.2, inplace=True)
        x1 = F.leaky_relu(self.conv1(x0), negative_slope=0.2, inplace=True)
        x2 = F.leaky_relu(self.conv2(x1), negative_slope=0.2, inplace=True)
        x3 = F.leaky_relu(self.conv3(x2), negative_slope=0.2, inplace=True)

        # upsample
        x3 = F.interpolate(x3, size=x2.shape[-2:], mode="bilinear", align_corners=False)
        # x3 = F.interpolate(x3, scale_factor=2, mode="bilinear", align_corners=False)
        x4 = F.leaky_relu(self.conv4(x3), negative_slope=0.2, inplace=True)

        if self.skip_connection:
            x4 = x4 + x2
        x4 = F.interpolate(x4, size=x1.shape[-2:], mode="bilinear", align_corners=False)
        # x4 = F.interpolate(x4, scale_factor=2, mode="bilinear", align_corners=False)
        x5 = F.leaky_relu(self.conv5(x4), negative_slope=0.2, inplace=True)

        if self.skip_connection:
            x5 = x5 + x1
        # x5 = F.interpolate(x5, scale_factor=2, mode="bilinear", align_corners=False)
        x5 = F.interpolate(x5, size=x0.shape[-2:], mode="bilinear", align_corners=False)
        x6 = F.leaky_relu(self.conv6(x5), negative_slope=0.2, inplace=True)

        if self.skip_connection:
            x6 = x6 + x0

        # extra
        out = F.leaky_relu(self.conv7(x6), negative_slope=0.2, inplace=True)
        out = F.leaky_relu(self.conv8(out), negative_slope=0.2, inplace=True)
        out = self.conv9(out)

        return out