//import React, { Component } from "react";
import React from "react";
import loading from "./loading.gif";

//export class Spinner extends Component { //Class Based Component
const Spinner = () => {
  //Function Based Component
  //render() {
  return (
    <div className="text-center">
      <img className="my-3" src={loading} alt="loading" />
    </div>
  );
  //}
};

export default Spinner;
