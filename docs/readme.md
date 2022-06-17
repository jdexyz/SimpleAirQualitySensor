# (A) Simple Air Quality Sensor



### Parts

All parts were bought from https://shop.pimoroni.com/

- [Adafruit MagTag - 2.9" Grayscale E-Ink WiFi Display](https://www.adafruit.com/product/4800)
- [Adafruit CCS811 Air Quality Sensor Breakout](https://www.adafruit.com/product/3566)
- [Adafruit PMSA003I Air Quality Breakout](https://www.adafruit.com/product/4632)
- [Adafruit SCD-41 - True CO2 Temperature and Humidity Sensor](https://www.adafruit.com/product/5190)
- [MICS6814 3-in-1 Gas Sensor Breakout (CO, NO2, NH3)](https://shop.pimoroni.com/products/mics6814-gas-sensor-breakout)
- [BME688 4-in-1 Air Quality Breakout](https://shop.pimoroni.com/products/bme688-breakout)
- [LiPo Battery Pack – 2000mAh](https://shop.pimoroni.com/products/lipo-battery-pack?variant=20429082247)



## A clueless but quick method for creating 3D boards from Eagle



At some point, with the integration of Eagle in Fusion 360, I thought I could open Eagle board files from Adafruit/Sparkfun and get in one click a 3D model in Fusion 360.

This did not happen. I spent a few hours trying to get the libraries right, but I am still confused and definitely not successful. However, I can quickly get the board with rough components placed, which is enough for me.

I ended up doing the following :

1. Open the board in Eagle. I used the latest version of Eagle as of March 2022, Eagle 9.6.

2. Click on the Manufacturing tab on the right. Click on the settings icon, and choose "SolderMask Color". Choose the appropriate color.

3. Click on the Fusion 360 tab to create a new board there.

4. In Fusion, open the generated model. 

5. Find the board packages, then right click and "Save a Copy".

6. Open the new Packages model, it is now a normal 3D model, instead of a 3D PCB.

7. In the data panel, click on the previous 3D PCB model and insert it in the current model.

8. Break the link of the inserted model and delete its packages.

9. Next clean up the model, removing the rectangle placeholders in front of holes, vias, etc.

10. Then import all 3D models of important parts manually. I only did this for big components that matter in mechanical assembly.

    