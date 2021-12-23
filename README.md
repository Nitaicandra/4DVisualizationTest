# 4DVisualizationTest

There are currently 2 main ways to visualize 4d objects, Stereographic projections and Crossection projections
Stereographic projections work by scaling the points of a 4d object based on the distance to some other point in space,  it can be thought of as taking a 3 dimensional shadow of 4d object.
![image](https://user-images.githubusercontent.com/89361982/147189608-e3ef338c-004e-4880-b800-cf42340b30d8.png)
![1p8 2021_12_23_(😦)(477)](https://user-images.githubusercontent.com/89361982/147190919-2c27579d-d29b-4b72-bc1c-fedfd3015c9c.png)

The second Method works like an MRI Scan but instead of taking 2d slices of a 3d object it takes 3d slices of a 4d object
![image](https://user-images.githubusercontent.com/89361982/147191103-54e314b7-4e03-4643-8b21-02ac2b573f0b.png)
Source: 4d Toys

the main issue with both of these projections is that they do not provide a satisfiying way to navigate a 4d environment. 
I believe that the solution to this is to define a 4d camera in space with a custom projection matrix. 
currently ive thought up 3 possible models that could 





This is a standard cube, notice how the back most face is farther to the right than the front most face when the cube moves left due to the perspective projection
![ezgif com-gif-maker-1](https://user-images.githubusercontent.com/89361982/139005143-31a2f04d-13e6-4420-839f-df152ec4d74f.gif)

This is a Stereographic projection of a Tesseract
![ezgif com-gif-maker](https://user-images.githubusercontent.com/89361982/139005135-2bb1e8b6-7517-4c36-87f6-61439cf98b9a.gif)



This is the same cube, notice how the inner cube does not move relative to the outer cube like you would expect following the logic of the perspective projection shown in the first image

![ezgif com-gif-maker-4](https://user-images.githubusercontent.com/89361982/139004725-e4ff6b14-746a-4a1a-9a19-24a3060e2921.gif)

This is an Artistic represention of how a perspective projection of a 4d cube would look like when viewed from the front
![ezgif com-gif-maker-2](https://user-images.githubusercontent.com/89361982/139004896-db6e215a-4a9e-4301-8295-21a8de6d9f57.gif)

This is the same cube viewed from a different angle

![ezgif com-gif-maker-3](https://user-images.githubusercontent.com/89361982/139004790-de6ebdeb-1e48-4295-b5b4-85b278def02d.gif)

