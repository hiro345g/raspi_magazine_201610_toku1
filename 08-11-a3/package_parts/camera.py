#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pygame
import pygame.camera
import shutil


class UsbWebCam:
    def __init__(self, camera_device='/dev/video0', size=(320, 240), file_path='usbwebcam.jpg', wait_time=100):
        self.camera_device = camera_device
        self.size = size
        self.file_path = file_path
        path, ext = os.path.splitext(file_path)
        self.src_file_name = "{0}_0{1}".format(path, ext)
        self.wait_time = wait_time
        self.running = False
        self.camera = None
        self.filter_app = []

    def __wait_for_camera(self):
        while not self.camera.query_image():  # カメラの撮影準備ができるまで待機
            pygame.time.wait(self.wait_time)  # wait_timeミリ秒待機
            if self.camera is None:
                break

    def start(self):
        if not self.running:
            pygame.init()
            pygame.camera.init()
            pygame.display.init()
            self.camera = pygame.camera.Camera(self.camera_device, self.size)  # カメラの用意
            self.camera.start()  # カメラ開始
            self.running = True
            print('UsbWebCam start')

    def capture(self):
        if self.running:
            self.__wait_for_camera()  # カメラの待機
            if self.camera is None:
                return
            snapshot = self.camera.get_image()  # 写真撮影
            pygame.image.save(snapshot, self.src_file_name)  # src_file_nameへ画像保存
            if len(self.filter_app) != 0:
                for app in self.filter_app:
                    app.filter(self.src_file_name)
            shutil.move(self.src_file_name, self.file_path)  # file_pathへファイル移動

    def stop(self):
        if self.running:
            if self.camera is not None:
                self.camera.stop()  # カメラ停止
                self.camera = None
            pygame.quit()  # pygame終了
            self.running = False
            print('UsbWebCam stop')

    def add_filter_app(self, app_obj):
        self.filter_app.append(app_obj)
