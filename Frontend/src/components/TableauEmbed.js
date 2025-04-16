// src/components/TableauEmbed.js
import React from "react";

function TableauEmbed({ url }) {
  return (
    <iframe
      src={url}
      width="100%"
      height="850"
      style={{ border: "none", marginBottom: "2rem" }}
      title="Tableau Dashboard"
      allowFullScreen
    />
  );
}

export default TableauEmbed;
