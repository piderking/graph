/*
 *
 * This file sets up our web app with 3D scene and communications.
 *
 */

import * as THREE from "three";
import { Communications } from "./communications.js";
import { OrbitControls } from './util/OrbitControls.js';
import { Cache } from "./cache.js";

let camera, renderer, scene;
let controls;
let communications;
let scene_size = 0;
let frameCount = 0;
let cache;
function init() {
  scene = new THREE.Scene();

  cache = new Cache();
  

  let width = window.innerWidth;
  let height = window.innerHeight;

  camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 5000);
  camera.position.set(0, 3, 6);
  scene.add(camera);
  scene.background = new THREE.Color( 255, 255, 255 );


  communications = new Communications(scene, cache)

  //THREE WebGL renderer
  renderer = new THREE.WebGLRenderer({
    antialiasing: true,
  });

  //renderer.setClearColor(new THREE.Color("lightblue"));
  renderer.setSize(width, height);
  
  
  /*
        // Test Lines
  const points = [
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(1.5, 1, 1),
  ]
  // Test THREEJS Code Here
  let line = new THREE.LineSegments(
    new THREE.BufferGeometry().setFromPoints(points),
    new THREE.LineBasicMaterial({ color: 1234, 	linewidth: 4 })
  )
    scene.add(line)
  */

  

  //Push the canvas to the DOM
  let domElement = document.getElementById("canvas-container");
  domElement.append(renderer.domElement);
  controls = new OrbitControls( camera, renderer.domElement );

  //Setup event listeners for events and handle the states
  window.addEventListener("resize", (e) => onWindowResize(e), false);
  
  // Controls

  // Helpers
  scene.add(new THREE.GridHelper(500, 500));
  scene.add(new THREE.AxesHelper(1));

  addLights();

  // Start the loop
  update();

  
}

init();

//////////////////////////////////////////////////////////////////////
// Lighting 💡
//////////////////////////////////////////////////////////////////////

function addLights() {
  scene.add(new THREE.AmbientLight(0xffffe6, 0.7));
}


function update() {
  //console.log(scene.children.length)
  requestAnimationFrame(() => update());
  frameCount++;  

  controls.update()

  renderer.render(scene, camera);
}

//////////////////////////////////////////////////////////////////////
// Event Handlers 🍽
//////////////////////////////////////////////////////////////////////

function onWindowResize(e) {
  let width = window.innerWidth;
  let height = Math.floor(window.innerHeight );
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}
