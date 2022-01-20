# 4DVisualizationTest
This project will discribe a new method for 4d projection

|The main way to visualize 4d objects currently is through stereographic projection.| 
|---|
![ezgif com-gif-maker](https://user-images.githubusercontent.com/89361982/139005135-2bb1e8b6-7517-4c36-87f6-61439cf98b9a.gif)

|You can think of a stereographic projections as casting a light on an object and then rendnering the shadow created from the result. This method can be generalized to 4d  |
|---|

|![image](https://user-images.githubusercontent.com/89361982/147189608-e3ef338c-004e-4880-b800-cf42340b30d8.png)|![1p8 2021_12_23_(😦)(477)](https://user-images.githubusercontent.com/89361982/147190919-2c27579d-d29b-4b72-bc1c-fedfd3015c9c.png)|
|---|---|

|Mathematically this is achieved by assigning an extra coordiante to each vertice (xyzw) and definig a "light source" with an arbitrary location in 4d space. Then you go into the local space of each object and divide each coordinate of every vertice by the w distance from the "light source".  Then you can discard the w coordinate and render the scene normally. This will result in verticies further away from the light source being shrunk towards the orgin of the object which is what creates the inner cube seen in a tesseract|
|---|
however the problem with this is that you cant visualze rotating the camera in 4d space because the camera is not define in 4d space only the light and cube are.
In addition to that it doesnt perserve the rules of perspective. For example here is a stereographic projection of a normal cube.
![JKIsabellinewheatear20_01_2022](https://user-images.githubusercontent.com/89361982/150290413-5ab6dd46-feab-455a-8a00-178f1476cbbf.gif)
This is a perspective projection of that same cube, notice how the back most face of the cube is farther to the right than the front most face when the cube moves left due to the perspective projection
![ezgif com-gif-maker-1](https://user-images.githubusercontent.com/89361982/139005143-31a2f04d-13e6-4420-839f-df152ec4d74f.gif)
This is the tesseract shown earlier, if it followed perspective then logically you would expect the inner cube to displace towards the right like the normal cube
![ezgif com-gif-maker-4](https://user-images.githubusercontent.com/89361982/139004725-e4ff6b14-746a-4a1a-9a19-24a3060e2921.gif)
Inorder to perserve this perspective effect and also allow for 4d camera movements ive come up with a new method of projection. Instead of simply dividing each coordinate by the distance to an arbitrary point you convert each point into the 4d camera's local coordinate frame(pointing in the zdirection) then project those vertices back into 3d space by using a 2 standard perspective matrices to project onto the zx and zy planes you would then use the x coordinates from the zx projection and the y coordinates of the zy poject and then discard the w, lastly you would multiply the new xyz coordinates left over in a standard projection matrix to get the final result
![ezgif com-gif-maker-2](https://user-images.githubusercontent.com/89361982/139004896-db6e215a-4a9e-4301-8295-21a8de6d9f57.gif)
This is the same cube viewed from a different angle
![ezgif com-gif-maker-3](https://user-images.githubusercontent.com/89361982/139004790-de6ebdeb-1e48-4295-b5b4-85b278def02d.gif)
currently im in the process of formalizing this method of projection mathematically. 
in order to achieve the effect of scaling the coordinates based on the displacement of local camera coordinates you must first define a orthonormal coordinate frame for the camera. however unlike in 3d you cannot use a cross product to find a perpendicualr vector from the camera  so instead you have to use the gram-schmidt process. this is the step im currently on.
  

