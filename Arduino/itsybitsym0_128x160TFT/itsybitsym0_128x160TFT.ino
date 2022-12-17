// Adafruit_ImageReader test for Adafruit ST7735 TFT Breakout for Arduino.
// Demonstrates loading images from SD card or flash memory to the screen,
// to RAM, and how to query image file dimensions.
// As written, this uses the microcontroller's SPI interface for the screen
// (not 'bitbang') and must be wired to specific pins (e.g. for Arduino Uno,
// MOSI = pin 11, MISO = 12, SCK = 13). Other pins are configurable below.

#include <Adafruit_GFX.h>         // Core graphics library
#include <Adafruit_ST7735.h>      // Hardware-specific library
#include <SdFat.h>                // SD card & FAT filesystem library
#include <Adafruit_SPIFlash.h>    // SPI / QSPI flash library
#include <Adafruit_ImageReader.h> // Image-reading functions

// Comment out the next line to load from SPI/QSPI flash instead of SD card:
#define USE_SD_CARD

// TFT display and SD card share the hardware SPI interface, using
// 'select' pins for each to identify the active device on the bus.

#define SD_CS    11 // SD card select pin
#define TFT_CS  10 // TFT select pin
#define TFT_DC   7 // TFT display/command pin
#define TFT_RST  9 // Or set to -1 and connect to Arduino RESET pin

#if defined(USE_SD_CARD)
  SdFat                SD;         // SD card filesystem
  Adafruit_ImageReader reader(SD); // Image-reader object, pass in SD filesys
#else
  // SPI or QSPI flash filesystem (i.e. CIRCUITPY drive)
  #if defined(__SAMD51__) || defined(NRF52840_XXAA)
    Adafruit_FlashTransport_QSPI flashTransport(PIN_QSPI_SCK, PIN_QSPI_CS,
      PIN_QSPI_IO0, PIN_QSPI_IO1, PIN_QSPI_IO2, PIN_QSPI_IO3);
  #else
    #if (SPI_INTERFACES_COUNT == 1)
      Adafruit_FlashTransport_SPI flashTransport(SS, &SPI);
    #else
      Adafruit_FlashTransport_SPI flashTransport(SS1, &SPI1);
    #endif
  #endif
  Adafruit_SPIFlash    flash(&flashTransport);
  FatVolume        filesys;
  Adafruit_ImageReader reader(filesys); // Image-reader, pass in flash filesys
#endif

Adafruit_ST7735      tft    = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);
Adafruit_Image       img;        // An image loaded into RAM
int32_t              width  = 0, // BMP image dimensions
                     height = 0;
int16_t               counter  = 0; // BMP image dimensions
char                 files[][10] =
{
"/a001.bmp",
"/a002.bmp",
"/a003.bmp",
"/a004.bmp",
"/a005.bmp",
"/a006.bmp",
"/a007.bmp",
"/a008.bmp",
"/a009.bmp",
"/a010.bmp",
"/a011.bmp",
"/a012.bmp",
"/a013.bmp",
"/a014.bmp",
"/a015.bmp",
"/a016.bmp",
"/a017.bmp",
"/a018.bmp",
"/a019.bmp",
"/a020.bmp",
"/a021.bmp",
"/a022.bmp",
"/a023.bmp",
"/a024.bmp",
"/a025.bmp",
"/a026.bmp",
"/a027.bmp",
"/a028.bmp",
"/a029.bmp",
"/a030.bmp",
"/a031.bmp",
"/a032.bmp",
"/a033.bmp",
"/a034.bmp",
"/a035.bmp",
"/a036.bmp",
"/a037.bmp",
"/a038.bmp",
"/a039.bmp",
"/a040.bmp",
"/a041.bmp",
"/a042.bmp",
"/a043.bmp",
"/a044.bmp",
"/a045.bmp",
"/a046.bmp",
"/a047.bmp",
"/a048.bmp",
"/a049.bmp",
"/a050.bmp",
"/a051.bmp",
"/a052.bmp",
"/a053.bmp",
"/a054.bmp",
"/a055.bmp",
"/a056.bmp",
"/a057.bmp",
"/a058.bmp",
"/a059.bmp",
"/a060.bmp",
"/a061.bmp",
"/a062.bmp",
"/a063.bmp",
"/a064.bmp",
"/a065.bmp",
"/a066.bmp",
"/a067.bmp",
"/a068.bmp",
"/a069.bmp",
"/a070.bmp",
"/a071.bmp",
"/a072.bmp",
"/a073.bmp",
"/a074.bmp",
"/a075.bmp",
"/a076.bmp",
"/a077.bmp",
"/a078.bmp",
"/a079.bmp",
"/a080.bmp",
"/a081.bmp",
"/a082.bmp",
"/a083.bmp",
"/a084.bmp",
"/a085.bmp",
"/a086.bmp",
"/a087.bmp",
"/a088.bmp",
"/a089.bmp",
"/a090.bmp",
"/a091.bmp",
"/a092.bmp",
"/a093.bmp",
"/a094.bmp",
"/a095.bmp",
"/a096.bmp",
"/a097.bmp",
"/a098.bmp",
"/a099.bmp",
"/a100.bmp",
"/a101.bmp",
"/a102.bmp",
"/a103.bmp",
"/a104.bmp",
"/a105.bmp",
"/a106.bmp",
"/a107.bmp",
"/a108.bmp",
"/a109.bmp",
"/a110.bmp",
"/a111.bmp",
"/a112.bmp",
"/a113.bmp",
"/a114.bmp",
"/a115.bmp",
"/a116.bmp",
"/a117.bmp",
"/a118.bmp",
"/a119.bmp",
"/a120.bmp",
"/a121.bmp",
"/a122.bmp",
"/a123.bmp",
"/a124.bmp",
"/a125.bmp",
"/a126.bmp",
"/a127.bmp",
"/a128.bmp",
"/a129.bmp",
"/a130.bmp",
"/a131.bmp",
"/a132.bmp",
"/a133.bmp",
"/a134.bmp",
"/a135.bmp",
"/a136.bmp",
"/a137.bmp",
"/a138.bmp",
"/a139.bmp",
"/a140.bmp",
"/a141.bmp",
"/a142.bmp",
"/a143.bmp",
"/a144.bmp",
"/a145.bmp",
"/a146.bmp",
"/a147.bmp",
"/a148.bmp",
"/a149.bmp",
"/a150.bmp",
"/a151.bmp",
"/a152.bmp",
"/a153.bmp",
"/a154.bmp",
"/a155.bmp",
"/a156.bmp",
"/a157.bmp",
"/a158.bmp",
"/a159.bmp",
"/a160.bmp",
"/a161.bmp",
"/a162.bmp",
"/a163.bmp",
"/a164.bmp",
"/a165.bmp",
"/a166.bmp",
"/a167.bmp",
"/a168.bmp",
"/a169.bmp",
"/a170.bmp",
"/a171.bmp",
"/a172.bmp",
"/a173.bmp",
"/a174.bmp",
"/a175.bmp",
"/a176.bmp",
"/a177.bmp",
"/a178.bmp",
"/a179.bmp",
"/a180.bmp",
"/a181.bmp",
"/a182.bmp",
"/a183.bmp",
"/a184.bmp",
"/a185.bmp",
"/a186.bmp",
"/a187.bmp",
"/a188.bmp",
"/a189.bmp",
"/a190.bmp",
"/a191.bmp",
"/a192.bmp",
"/a193.bmp",
"/a194.bmp",
"/a195.bmp",
"/a196.bmp",
"/a197.bmp",
"/a198.bmp",
"/a199.bmp",
"/a200.bmp",
"/a201.bmp",
"/a202.bmp",
"/a203.bmp",
"/a204.bmp",
"/a205.bmp",
"/a206.bmp",
"/a207.bmp"
};

void setup(void) {

  ImageReturnCode stat; // Status from image-reading functions

  Serial.begin(9600);
#if !defined(ESP32)
//  while(!Serial);       // Wait for Serial Monitor before continuing
#endif

  tft.initR(INITR_BLACKTAB); // Initialize screen

  // The Adafruit_ImageReader constructor call (above, before setup())
  // accepts an uninitialized SdFat or FatVolume object. This MUST
  // BE INITIALIZED before using any of the image reader functions!
  Serial.print(F("Initializing filesystem..."));
#if defined(USE_SD_CARD)
  // SD card is pretty straightforward, a single call...
  if(!SD.begin(SD_CS, SD_SCK_MHZ(10))) { // Breakouts require 10 MHz limit due to longer wires
    Serial.println(F("SD begin() failed"));
    for(;;); // Fatal error, do not continue
  }
#else
  // SPI or QSPI flash requires two steps, one to access the bare flash
  // memory itself, then the second to access the filesystem within...
  if(!flash.begin()) {
    Serial.println(F("flash begin() failed"));
    for(;;);
  }
  if(!filesys.begin(&flash)) {
    Serial.println(F("filesys begin() failed"));
    for(;;);
  }
#endif
  Serial.println(F("OK!"));

  // Fill screen blue. Not a required step, this just shows that we're
  // successfully communicating with the screen.
  tft.fillScreen(ST7735_BLUE);

  // Load full-screen BMP file '001.bmp' at position (0,0) (top left).
  // Notice the 'reader' object performs this, with 'tft' as an argument.
  Serial.print(F("Loading parrot.bmp to screen..."));
  stat = reader.drawBMP("/001.bmp", tft, 0, 0);
  reader.printStatus(stat);   // How'd we do?

  // Query the dimensions of image '001.bmp' WITHOUT loading to screen:
  Serial.print(F("Querying 001.bmp image size..."));
  stat = reader.bmpDimensions("/001.bmp", &width, &height);
  reader.printStatus(stat);   // How'd we do?
  if(stat == IMAGE_SUCCESS) { // If it worked, print image size...
    Serial.print(F("Image dimensions: "));
    Serial.print(width);
    Serial.write('x');
    Serial.println(height);
  }

  delay(2000); // Pause 2 seconds before moving on to loop()
}

void loop() {
  if (counter == 207) counter = 0;
  Serial.print("showing image: ");
  Serial.println(files[counter]);
  reader.drawBMP(files[counter], tft, 0, 0);
  counter = counter + 1;
  delay(5000); // Pause 5 sec.
}
