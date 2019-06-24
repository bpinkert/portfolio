import win32gui
import win32ui
import win32con
import win32api

# grab main desktop window
hdesktop = win32gui.GetDesktopWindow()

# determine size of monitors in px
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# create a device context
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# create memory based context
mem_dc = img_dc.CreateCompatibleDC()

# create bitmap object
screenshot = win32ui.CreateBitMap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# copy screen into memory device context
mem_dc.Bitblt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# save the bitmap to file
screenshot.SaveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

# free our objects
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
