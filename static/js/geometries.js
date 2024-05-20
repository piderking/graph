import * as THREE from "three";
/**
 * Represents a 3D Box.
 * @constructor
 * @param {THREE.Scene} scene - THREE.JS Scene
 * @param {object} scale - x, y, z of the scale, default to 1
 * @param {object} position - x, y, z of the box, default to 
 */
export class Box{
    constructor(scene, uuid, scale, position, color){
        this.scene = scene;
        this.scale = scale
        this.position = position
        this.color = color
        // Geometric things
        this._geo = new THREE.BoxGeometry(scale.x, scale.y, scale.z);
        this._mat = new THREE.MeshBasicMaterial({
            color: this.color
        });
        this._mesh = new THREE.Mesh(this._geo, this._mat);
        
        this._mesh.position.set(position.x, position.y, position.z);
        
        // Set ID
        this.uuid = uuid;
        this._mesh.uuid = uuid;

        // Add to Scene
        this.scene.add(this._mesh)
    }
    object(){
        return this._mesh
    }
    move(x, y, z){
        this._mesh?.position.set(x, y, z);
    }
    
    bremove(){
        this._geo.dispose();
        this._mat.dispose();
        this.scene.remove( this._mesh );
        console.log(`Box Removed of UUID: ${this.uuid}`)
    }
}
export class Points{
    setSize(new_size){
        this.size = new_size
        this._mat.size = this.size

    }
    setColor(new_color){
        this.color = new_color
        this._mat.color = this.color

    }
    constructor(scene, uuid, scale, position, points, color, size){
        this.color = color
        this.scene = scene;
        this.scale = scale
        this.position = position
        this.size = size

        this._mat =  new THREE.PointsMaterial({
            color: this.color
        })
        this._mat.size = size
        this._mesh = new THREE.Points(
            new THREE.BufferGeometry().setAttribute("position", new THREE.BufferAttribute(
                new Float32Array( 
                    points
                ), 3
            )),
           this._mat
        )

        this._mesh.scale.set(scale, scale, scale)
        this._mesh.position.set(position.x, position.y, position.z)
        
        // Set ID and set meshes ID to it
        this.uuid = uuid;
        this._mesh.uuid = uuid;

        // Add to Scene
        this.scene.add(this._mesh)

    }
    object(){
        return this._mesh
    }
    move(x, y, z){
        this._mesh?.position.set(x, y, z);
    }
    
    bremove(){
        this._geo.dispose();
        this._mat.dispose();
        this.scene.remove( this._mesh );
        console.log(`Point Clouod Removed of UUID: ${this.uuid}`)
    }
}