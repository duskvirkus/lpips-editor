import lpips


class LpipsRunner:

    def __init__(self, use_gpu):
        self.use_gpu = use_gpu

        self.loss_fn = lpips.LPIPS(net='alex', version='0.1')
        if self.use_gpu:
            self.loss_fn.cuda()

    def eval(self, image0, image1):
        img0 = lpips.im2tensor(image0[:, :, ::-1])
        if self.use_gpu:
            img0 = img0.cuda()
        img1 = lpips.im2tensor(image1[:, :, ::-1])
        if self.use_gpu:
            img1 = img1.cuda()
        return self.loss_fn.forward(img0, img1).item()
