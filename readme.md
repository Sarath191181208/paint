
# Paint

A simple pixel art application in **python** using **pygame** inspired by microsoft paint from windows xp.

# Description

Works on a basic priciple of displays that all display is rows,columns of contigious blocks.
All the blocks are objects having a color property, are placed in a 2D grid. All the features are just array problems.

## Demo

![Image](https://github.com/Sarath191181208/paint/blob/master/images/Screenshot.png)

  
## Features

- A brush tool to draw on canvas.
- An eraser toool to erase on canvas.
- An Line tool which draws lines/ L shaped lines taking two points as a reference.
- A fill tool which fills a certain closed area.
- A Color Picker tool which when selected and clicked on canvas selects the color. 
- Save/Load.
- Undo/Redo.
- Toggle zoom screen on/off button.
- Clear Screen button.
- Left click to select the color and Right ot change the color.
- A slider the adjust the size of brush.
- Right click on canvas becomes Eraser.
  
## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/paint
```

Go to the project directory

```bash
  cd ./paint
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

  ## References

Pyint_Pixel-Painter from Burakcoli : https://github.com/Burakcoli/Pyint_Pixel-Painter

Tech With Tim : https://www.youtube.com/watch?v=N20eXcfyQ_4

Icons:
These icons are picked from Internet.
Made the Line icon myself.
## Usage
 - **Right click the color block to change its color.**
 - Left click the color block to select a color.
 - The selected color will have a outline around it.
 - All the tools are similar to Microsoft Paint.
 - Line tool is Unique, place two points and it draws a "L" between these points.
 
 
## Hot keys

- Z : Undo
- Y : Redo
- C : Clear
- S : Save
- O : Load
- G : Toggle Grid

- F : Change to Fill tool.
- E : Change to Eraser tool.
- L : Change to Line tool.
- P : Change to Pen tool.

## Requirements
- python ``` Make sure to add to path ```
- pygame  ``` pip install pygame ```
- tkinter ``` default ```

  