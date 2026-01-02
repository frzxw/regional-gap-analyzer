"use client";

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix for default marker icons in Leaflet with Next.js
// eslint-disable-next-line @typescript-eslint/no-explicit-any
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Center of Indonesia
const DEFAULT_CENTER: LatLngExpression = [-2.5, 118.0];
const DEFAULT_ZOOM = 5;

// Demo markers for some provinces (DEMO DATA ONLY)
const DEMO_MARKERS: Array<{
  position: LatLngExpression;
  name: string;
  code: string;
}> = [
  { position: [-6.2088, 106.8456], name: "DKI Jakarta", code: "ID-JK" },
  { position: [-7.7956, 110.3695], name: "DI Yogyakarta", code: "ID-YO" },
  { position: [-6.9175, 107.6191], name: "Jawa Barat", code: "ID-JB" },
  { position: [-7.2504, 112.7688], name: "Jawa Timur", code: "ID-JI" },
  { position: [-8.6500, 115.2167], name: "Bali", code: "ID-BA" },
  { position: [3.5952, 98.6722], name: "Sumatera Utara", code: "ID-SU" },
  { position: [-5.1477, 119.4327], name: "Sulawesi Selatan", code: "ID-SN" },
];

export default function MapComponent() {
  return (
    <div className="h-96 rounded-lg overflow-hidden border border-gray-200">
      <MapContainer
        center={DEFAULT_CENTER}
        zoom={DEFAULT_ZOOM}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Demo markers */}
        {DEMO_MARKERS.map((marker) => (
          <Marker key={marker.code} position={marker.position}>
            <Popup>
              <div className="text-center">
                <strong className="text-sm">{marker.name}</strong>
                <br />
                <span className="text-xs text-gray-500">{marker.code}</span>
                <br />
                <span className="text-xs text-blue-600">
                  Click for details (TODO)
                </span>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
