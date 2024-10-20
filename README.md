![logo](https://github.com/home-assistant/brands/blob/master/custom_integrations/iiyama_sicp/logo.png?raw=true)

# iiyama rs232 SICP

Library to control iiama TV over LAN using rs232 serial interface communication protocol.

Supported features depend on the model of the TV.

## Commands

| Hex Code | Type | Description                 | Additional Information |
|----------|------|-----------------------------|------------------------|
| 0x00     |      | Communication Control       | Generic report         |
| 0x15     | Get  | Serial Code                 |                        |
| 0x18     | Set  | Power state                 |                        |
| 0x19     | Get  | Power state                 |                        |
| 0x1C     | Set  | User Input Control          |                        |
| 0x1D     | Get  | User Input Control          |                        |
| 0x32     | Set  | Video parameters            |                        |
| 0x33     | Get  | Video parameters            | Brightness, etc.       |
| 0x34     | Set  | Color temperature           |                        |
| 0x35     | Get  | Color temperature           |                        |
| 0x36     | Set  | Color parameters            |                        |
| 0x37     | Get  | Color parameters            |                        |
| 0x3A     | Set  | Picture Format              |                        |
| 0x3B     | Get  | Picture Format              |                        |
| 0x42     | Set  | Audio parameters            |                        |
| 0x43     | Get  | Audio parameters            |                        |
| 0x44     | Set  | Volume                      |                        |
| 0x45     | Get  | Volume                      |                        |
| 0x5A     | Set  | Scheduling                  |                        |
| 0x5B     | Get  | Scheduling                  |                        |
| 0x70     |      | Auto Adjust                 | VGA only               |
| 0xAC     | Set  | Input Source                |                        |
| 0xAD     | Get  | Current Source              |                        |
| 0xAE     | Set  | Auto Signal Detecting       |                        |
| 0xAF     | Get  | Auto Signal Detecting       |                        |
| 0xA2     | Get  | Platform and version labels |                        |
| 0xA3     | Set  | Power state at cold start   |                        |
| 0xA4     | Get  | Power state at cold start   |                        |
| 0xB1     | Get  | Pixel Shift                 |                        |
| 0xB2     | Set  | Pixel Shift                 |                        |
| 0xB8     | Set  | Volume limits               |                        |
| 0xC0     | Get  | Language                    |                        |
| 0xC1     | Set  | Language                    |                        |
| 0xDB     |      | IR Remote                   |                        |
| 0x0F     |      | Miscellaneous info          | Operating hours        |

## IR codes

| Hex Code | IR Code      |
|----------|--------------|
| 0xA0     | Power        |
| 0xA1     | Menu         |
| 0xA2     | Input        |
| 0xA3     | Vol_Up       |
| 0xA4     | Vol_Down     |
| 0xA5     | Mute         |
| 0xA6     | Cursor_Up    |
| 0xA7     | Cursor_Down  |
| 0xA8     | Cursor_Left  |
| 0xA9     | Cursor_Right |
| 0xB1     | OK           |
| 0xB2     | Return       |
| 0xC1     | Red          |
| 0xC2     | Green        |
| 0xC3     | Yellow       |
| 0xC4     | Blue         |
| 0xD1     | Format       |
| 0xD2     | Info         |
| 0x00     | Btn_0        |
| 0x01     | Btn_1        |
| 0x02     | Btn_2        |
| 0x03     | Btn_3        |
| 0x04     | Btn_4        |
| 0x05     | Btn_5        |
| 0x06     | Btn_6        |
| 0x07     | Btn_7        |
| 0x08     | Btn_8        |
| 0x09     | Btn_9        |

## Input sources

| Hex Code | Input Source               |
|----------|----------------------------|
| 0x00     | Card DVI-D                 |
| 0x00     | Card OPS                   |
| 0x00     | COMPONENT                  |
| 0x00     | HDMI                       |
| 0x00     | VGA                        |
| 0x00     | VIDEO                      |
| 0x01     | CVI 2 (not applicable)     |
| 0x01     | Display Port               |
| 0x01     | DVI-D                      |
| 0x01     | S-VIDEO                    |
| 0x01     | USB                        |
| 0x01     | VIDEO                      |
| 0x02     | S-VIDEO                    |
| 0x03     | COMPONENT                  |
| 0x03     | CVI 2 (not applicable)     |
| 0x04     | CVI 2 (not applicable)     |
| 0x05     | VGA                        |
| 0x06     | HDMI 2                     |
| 0x07     | Card DVI-D                 |
| 0x07     | Display Port               |
| 0x07     | Display Port 2             |
| 0x08     | Card OPS                   |
| 0x08     | USB                        |
| 0x08     | USB 2                      |
| 0x09     | Card DVI-D                 |
| 0x09     | DVI-D                      |
| 0x09     | HDMI                       |
| 0x0A     | Display Port 1             |
| 0x0B     | Card OPS                   |
| 0x0C     | USB 1                      |
| 0x0D     | HDMI                       |
| 0x0d     | HDMI 1                     |
| 0x0E     | DVI-D                      |
| 0x0F     | HDMI 3                     |
| 0x10     | BROWSER                    |
| 0x11     | SMARTCMS                   |
| 0X12     | DMS (Digital Media Server) |
| 0x13     | INTERNAL STORAGE           |
| 0x14     | Reserved                   |
| 0x15     | Reserved                   |
| 0x16     | Media Player               |
| 0x17     | PDF Player                 |
| 0x18     | Custom                     |
| 0x19     | HDMI 4                     |
