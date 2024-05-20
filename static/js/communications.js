import * as THREE from "three";
import {Box, Points} from "./geometries.js"
export class Communications {

    constructor(scene){
        this.userDefinedCallbacks = {}
        this.scene = scene
        this.synced = false
        this.objects = []
        this.socket = io("/", {
          reconnectionDelayMax: 10000,
          auth: {
            token: ""
          },
          query: {
            "my-key": "my-value"
          }
        });
        

        this.initSocketConnection()
 
        

    }
    initSocketConnection() {
      
      console.log("Initializing socket.io...");
      this.socket.on("connect", () => {
        console.log("My socket ID:", this.socket.id);
      });
      console.log("SocketIO Initalized... Informing")
      this.socket.emit("init", {}) // No Objects saved locally yet

      console.log("Trying to Sync Data")
      this.socket.on("sync", (data)=>{
        if (this.synced){
          console.error("Already Synced")
          return
        }
        this.synced = true // So more syncs can't accidenatally be sent
        console.log("Starting Sync of Data")
        console.log(`Amount of objects to sync: ${data.len}`)
        console.log(`Client UUID: ${data.sid}... Matches: ${"True" ? data.sid == this.socket.id : "False"}`)
        console.log(data.objects)
        const objects = data.objects
        // TODO Add Objects Here (Assume Everything is being added)
        
        objects.forEach((object) => {
          switch (object.type){
            case "box":
              this.addBox(object.scale, object.position, object.color)
            case "point cloud":
              this.addPointCloud(object.scale, object.position, object.points, object.color, object.size)
          }
        })
        
        // Now Accept New Objects
        this.sit()
      })


    }
    async sit(){
      console.log("Waiting on events..")
      // Kill Event
      this.socket.on("kill", (data)=>{
        window.close()
      })
      this.socket.on("text", (data)=> {
        document.getElementById("info").innerText = data.text
        document.getElementById("info").style.visibility = "visible"

        setTimeout(()=>{
          document.getElementById("info").style.visibility = "hidden"

        },data.time)
      })

      // Box Event
      this.socket.on("box", (data)=>{
        console.log(`Box Event of Type ${data.event}`)
        if(data.event == "add"){
          console.log("Adding Box")
          this.addBox(data.scale, data.position, data.color)
        } else if (data.event == "remove"){
          this.objects.forEach((box, index)=>{
            if (box.uuid == data.uuid){
              this.box[index].bremove()
              return
            }
          })
        } else if (data.event == 'move'){
          this.objects.forEach((box, index)=>{
            if (box.uuid == data.uuid){
              this.box[index].move(data.position.x, data.position.y, data.position.z )
              return
            }
          })
        }
        
      })
      // Point CLoud Event
      this.socket.on("point", (data)=>{
        console.log(`Point Cloud Event of Type ${data.event}`)
        if(data.event == "add"){
          console.log("Adding Point Cloud")
          this.addPointCloud(data.scale, data.position, data.points, data.color, data.size)
        } else if (data.event == "remove"){
          this.object.forEach((pc, index)=>{
            if (pc.uuid == data.uuid){
              this.box[pc].bremove()
              return
            }
          })
        } else if (data.event == 'move'){
          this.object.forEach((pc, index)=>{
            if (pc.uuid == data.uuid){
              this.pc[index].move(data.position.x, data.position.y, data.position.z )
              return
            }
          })
        }
        
      })
      

    }
    addBox(scale, position, color){
      this.objects.push(new Box(this.scene, scale, position, color ))
    }
    removeBox(id){
      const object = scene.getObjectByProperty( 'uuid', id );

      object.geometry.dispose();
      object.material.dispose();
      this.scene.remove( object );
      // TODO Remove from list
    }
    
    addPointCloud(scale, position, points, color, size){
      //this.objects.push(new Points(this.scene, scale, position, points, color, size))
      this.objects.push(new Points(this.scene, scale, position, points, color, size))
    }
    removePointCloud(id){
      const object = scene.getObjectByProperty( 'uuid', id );

      object.geometry.dispose();
      object.material.dispose();
      this.scene.remove( object );
    }
    


}


/*
    // add a callback for a given event
    on(event, callback) {
      console.log(`Setting ${event} callback.`);
      this.userDefinedCallbacks[event].push(callback);
    }
  
    sendPosition(position) {
      this.socket?.emit("move", position);
    }
  
    sendData(data) {
      this.socket?.emit("data", data);
    }
  
    callEventCallback(event, data) {
      this.userDefinedCallbacks[event].forEach((callback) => {
        callback(data);
      });
    } */
