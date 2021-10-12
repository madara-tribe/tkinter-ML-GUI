import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import font
import time


class Application(tk.Frame):
    def __init__(self, master, video_source=0):
        super().__init__(master)
        self.master.geometry("1550x1000")
        self.master.title("Tkinter with Video Streaming and Capture")

        # Font
        self.font_frame = font.Font( family="Meiryo UI", size=15, weight="normal" )
        self.font_btn_big = font.Font( family="Meiryo UI", size=20, weight="bold" )
        self.font_btn_small = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_bigger = font.Font( family="Meiryo UI", size=45, weight="bold" )
        self.font_lbl_big = font.Font( family="Meiryo UI", size=30, weight="bold" )
        self.font_lbl_middle = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_small = font.Font( family="Meiryo UI", size=12, weight="normal" )
        
        self.vcap = cv2.VideoCapture( video_source )
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT )

        # Widget
        self.create_widgets()
        self.delay = 15 #[ms]
        self.update()


    def create_widgets(self):
        #Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text = 'Camera', font=self.font_frame)
        self.frame_cam.place(x = 10, y = 10)
        self.frame_cam.configure(width = self.width+30, height = self.height+50)
        self.frame_cam.grid(rowspan=8, column=1, row=0, padx = 10, pady=10)
        
        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(rowspan=8, column=1, row=0, padx = 10, pady=10)


        # Scale Gain Gain
        self.scale_gain_gain_var = tk.DoubleVar()
        self.scale_gain_gain_var.set(0)
        scaleH_gain_gain = tk.Scale( self.master, variable = self.scale_gain_gain_var, command = self.gain_gain_slider_scroll,
                                     label = 'Gain Gain',
                                     orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                     from_ = 0, to = 255, resolution=0.5, tickinterval=50)
        scaleH_gain_gain.grid(column=0, row=0, padx=5, pady=5)

        # Scale Gain AutoLight
        self.scale_gain_light_var = tk.DoubleVar()
        self.scale_gain_light_var.set(255)
        scaleH_gain_light = tk.Scale( self.master, variable = self.scale_gain_light_var, command = self.gain_light_slider_scroll,
                                      label = 'Gain AutoLightTarget',
                                      orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                      from_ = 0, to = 255, resolution=0.5, tickinterval=50)
        scaleH_gain_light.grid(column=0, row=1, padx=5, pady=5)

        # Scale BalanceWhite Red
        self.scale_bw_red_var = tk.DoubleVar()
        self.scale_bw_red_var.set(197)
        scaleH_bw_red = tk.Scale( self.master, variable = self.scale_bw_red_var, command = self.bw_red_slider_scroll,
                                  label = 'BalanceWhiteRed',
                                  orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                  from_ = 0, to = 511, resolution=0.5, tickinterval=200)
        scaleH_bw_red.grid(column=0, row=2, padx=5, pady=5)

        # Scale BalanceWhite Green
        self.scale_bw_green_var = tk.DoubleVar()
        self.scale_bw_green_var.set(136)
        scaleH_bw_green = tk.Scale( self.master, variable = self.scale_bw_green_var, command = self.bw_green_slider_scroll,
                                    label = 'BalanceWhiteGreen',
                                    orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                    from_ = 0, to = 511, resolution=0.5, tickinterval=200)
        scaleH_bw_green.grid(column=0, row=3, padx=5, pady=5)

        # Scale BalanceWhite Blue
        self.scale_bw_blue_var = tk.DoubleVar()
        self.scale_bw_blue_var.set(368)
        scaleH_bw_blue = tk.Scale( self.master, variable = self.scale_bw_blue_var, command = self.bw_blue_slider_scroll,
                                   label = 'BalanceWhiteBlue',
                                   orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                   from_ = 0, to = 511, resolution=0.5, tickinterval=200)
        scaleH_bw_blue.grid(column=0, row=4, padx=5, pady=5)
        
        # Scale BalanceWhite GreenR
        self.scale_bw_greenr_var = tk.DoubleVar()
        self.scale_bw_greenr_var.set(136)
        scaleH_bw_greenr = tk.Scale( self.master, variable = self.scale_bw_greenr_var, command = self.bw_greenr_slider_scroll,
                                     label = 'BalanceWhiteGreenR',
                                     orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                     from_ = 0, to = 511, resolution=0.5, tickinterval=200)
        scaleH_bw_greenr.grid(column=0, row=5, padx=5, pady=5)

        # Scale BalanceWhite GreenB
        self.scale_bw_greenb_var = tk.DoubleVar()
        self.scale_bw_greenb_var.set(141)
        scaleH_bw_greenb = tk.Scale( self.master, variable = self.scale_bw_greenb_var, command = self.bw_greenb_slider_scroll,
                                     label = 'BalanceWhiteGreenB',
                                     orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                     from_ = 0, to = 511, resolution=0.5, tickinterval=200)
        scaleH_bw_greenb.grid(column=0, row=6, padx=5, pady=5)

        # Scale zoom
        self.scale_zoom_var = tk.DoubleVar()
        self.scale_zoom_var.set(1.1)
        scaleH_zoom = tk.Scale( self.master, variable = self.scale_zoom_var, command = self.zoom_slider_scroll,
                                     label = 'Zoom',
                                     orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                     from_ = 1, to = 5, resolution=0.1, tickinterval=1)
        scaleH_zoom.grid(column=0, row=7, padx=5, pady=5)

        # Scale delay
        self.scale_delay_var = tk.DoubleVar()
        self.scale_delay_var.set(10)
        scaleH_delay = tk.Scale( self.master, variable = self.scale_delay_var, command = self.delay_slider_scroll,
                                     label = 'Delay for track speed(default=1)',
                                     orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                     from_ = 1, to = 20, resolution=1, tickinterval=2)
        scaleH_delay.grid(column=2, row=0, padx=5, pady=5)


        # Scope rect or arrow
        self.scale_scope_var = tk.DoubleVar()
        self.scale_scope_var.set(0)
        self.scaleH_scope = tk.Scale( self.master, variable = self.scale_scope_var, command = self.scope_slider_scroll,
                                           label = 'Scope',
                                           orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                           from_ = 0, to = 1, resolution=1, tickinterval=1)
        self.scaleH_scope.grid(column=2, row=1, padx=5, pady=5)

        # Upper border(y1)
        self.scale_upperborder_var = tk.DoubleVar()
        self.scale_upperborder_var.set(0.4)
        self.scaleH_upperborder = tk.Scale( self.master, variable = self.scale_upperborder_var, command = self.upperborder_slider_scroll,
                                            label = 'UpperBorder',
                                            orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                            from_ = 0, to = 0.4, resolution=0.1, tickinterval=0.1)
        self.scaleH_upperborder.grid(column=2, row=2, padx=5, pady=5)

        # Lower border(y2)
        self.scale_lowerborder_var = tk.DoubleVar()
        self.scale_lowerborder_var.set(0.9)
        self.scaleH_lowerborder = tk.Scale( self.master, variable = self.scale_lowerborder_var, command = self.lowerborder_slider_scroll,
                                            label = 'LowerBorder',
                                            orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                            from_ = 0.6, to = 1.0, resolution=0.1, tickinterval=0.1)
        self.scaleH_lowerborder.grid(column=2, row=3, padx=5, pady=5)

        # Right border(x1)
        self.scale_rightborder_var = tk.DoubleVar()
        self.scale_rightborder_var.set(0.0)
        self.scaleH_rightborder = tk.Scale( self.master, variable = self.scale_rightborder_var, command = self.rightborder_slider_scroll,
                                            label = 'RightBorder',
                                            orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                            from_ = 0, to = 0.4, resolution=0.1, tickinterval=0.1)
        self.scaleH_rightborder.grid(column=2, row=4, padx=5, pady=5)

        # Left border(x2)
        self.scale_leftborder_var = tk.DoubleVar()
        self.scale_leftborder_var.set(1.0)
        self.scaleH_leftborder = tk.Scale( self.master, variable = self.scale_leftborder_var, command = self.leftborder_slider_scroll,
                                           label = 'LeftBorder',
                                           orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                           from_ = 0.6, to = 1.0, resolution=0.1, tickinterval=0.1)
        self.scaleH_leftborder.grid(column=2, row=5, padx=5, pady=5)

        # Debug or projection
        self.scale_projection_var = tk.DoubleVar()
        self.scale_projection_var.set(20)
        self.scaleH_projection = tk.Scale( self.master, variable = self.scale_projection_var, command = self.projection_slider_scroll,
                                           label = 'Delay for projection',
                                           orient=tk.HORIZONTAL, length = 250, width = 20, sliderlength = 20,
                                           from_ = 1, to = 100, resolution=5, tickinterval=20)
        self.scaleH_projection.grid(column=2, row=6, padx=6, pady=5)


    def update(self):
        _, frame = self.vcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))

        #self.photo -> Canvas
        self.canvas1.create_image(0,0, image= self.photo, anchor = tk.NW)
        self.master.after(self.delay, self.update)


    def press_snapshot_button(self):
        self.master.destroy()

    def press_close_button(self):
        self.master.destroy()


    def gain_gain_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_gain_gain_var.get())


    def gain_light_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_gain_light_var.get())


    def bw_red_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_bw_red_var.get())
    

    def bw_green_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_bw_green_var.get())


    def bw_blue_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_bw_blue_var.get())


    def bw_greenr_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_bw_greenr_var.get())


    def bw_greenb_slider_scroll(self, event=None):
        '''Value of the slider'''
        return int(self.scale_bw_greenb_var.get())


    def zoom_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_zoom_var.get())


    def delay_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_delay_var.get())


    def projection_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_projection_var.get())


    def scope_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_scope_var.get())


    def upperborder_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_upperborder_var.get())


    def lowerborder_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_lowerborder_var.get())


    def rightborder_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_rightborder_var.get())


    def leftborder_slider_scroll(self, event=None):
        '''Value of the slider'''
        return float(self.scale_leftborder_var.get())


    def set_init_param(self, gain_light_value, balance_lst):
        red, green, blue, greenr, greenb = balance_lst
        self.scale_gain_light_var.set(gain_light_value)
        self.scale_bw_red_var.set(int(red))
        self.scale_bw_green_var.set(int(green))
        self.scale_bw_blue_var.set(int(blue))
        self.scale_bw_greenr_var.set(int(greenr))
        self.scale_bw_greenb_var.set(int(greenb))
        return

    def set_init_border(self, x1, y1, x2, y2):
        self.scale_rightborder_var.set(int(x1))
        self.scale_upperborder_var.set(int(y1))
        self.scale_leftborder_var.set(int(x2))
        self.scale_lowerborder_var.set(int(y2))
        return

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)#Inherit
    app.mainloop()
