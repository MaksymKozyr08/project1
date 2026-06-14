// F1 Autonomous Line-Following Visualizer
// Core simulation logic using Three.js

// Global variables for main scene
let scene, camera, renderer, orbitControls;
let mainTrackMesh, mainLineMesh, mainCurbLMesh, mainCurbRMesh, startGridMesh;
let car;
let activeCurve, activeTrackId;
let clock;

// Simulation settings & state
const simState = {
  activeTrack: 'monaco',
  trackWidth: 2.4,
  complexity: 4,
  targetSpeed: 120, // km/h
  autonomous: true,
  cameraMode: 'orbital', // orbital, top, chase, driver
  
  // PID Steering
  kp: 3.5,
  ki: 0.05,
  kd: 1.2,
  sensorOffset: 1.5, // meters ahead of car
};

// Physics state of the car
const carState = {
  position: new THREE.Vector3(),
  yaw: 0,
  speed: 0, // current speed in units/sec (1 unit = 1 meter approx)
  steerAngle: 0,
  closestT: 0,
  
  // PID accumulators
  prevSensorError: 0,
  integralError: 0,
  
  // Lap timing
  lapStartTime: 0,
  lapHalfway: false,
  bestLapTime: Infinity,
  lapCount: 0,
  
  // Telemetry logs
  cteSum: 0,
  cteCount: 0,
  maxSpeedReached: 0,
  
  // Manual driving controls
  keys: {
    forward: false,
    backward: false,
    left: false,
    right: false
  }
};

// SVG Telemetry Chart history
const cteHistory = [];
const maxCteHistoryLength = 50;

// Track specifications
const tracksConfig = {
  monaco: {
    name: "Monaco GP",
    location: "Monte Carlo, Monaco",
    lengthStr: "3.337 km",
    points: [
      new THREE.Vector3(0, 0, 30),     // Start/Finish straight
      new THREE.Vector3(20, 0, 30),    // Sainte Devote
      new THREE.Vector3(25, 2.5, 12),  // Beau Rivage (uphill)
      new THREE.Vector3(20, 4.0, 0),     // Massenet
      new THREE.Vector3(12, 3.5, -8),    // Casino Square
      new THREE.Vector3(5, 1.8, -15),    // Mirabeau Haute
      new THREE.Vector3(-5, 0, -20),   // Grand Hotel Hairpin (downhill, lowest point)
      new THREE.Vector3(-12, -0.5, -15), // Mirabeau Bas
      new THREE.Vector3(-16, 0, -8),   // Portier
      new THREE.Vector3(-8, 0.8, 5),     // Tunnel Entrance
      new THREE.Vector3(5, 0.8, 15),     // Tunnel Exit / Chicane straight
      new THREE.Vector3(-2, 0, 18),    // Nouvelle Chicane
      new THREE.Vector3(-10, 0, 22),   // Tabac
      new THREE.Vector3(-18, 0, 18),   // Swimming Pool entry
      new THREE.Vector3(-25, 0, 25),   // Swimming Pool exit
      new THREE.Vector3(-18, 0, 32),   // Rascasse
      new THREE.Vector3(-10, 0, 30),   // Anthony Noghes
    ]
  },
  monza: {
    name: "Monza GP",
    location: "Monza, Italy",
    lengthStr: "5.793 km",
    points: [
      new THREE.Vector3(-35, 0, 20),   // Start straight
      new THREE.Vector3(10, 0, 20),    // Rettifilo entry
      new THREE.Vector3(14, 0, 23),    // Rettifilo Chicane
      new THREE.Vector3(17, 0, 20),    
      new THREE.Vector3(30, 0, 8),    // Curva Grande
      new THREE.Vector3(34, 0, -6),
      new THREE.Vector3(30, 0, -20),   // Roggia Chicane
      new THREE.Vector3(26, 0, -18),
      new THREE.Vector3(22, 0, -20),
      new THREE.Vector3(10, 0, -30),   // Lesmo 1
      new THREE.Vector3(0, 0, -32),    // Lesmo 2
      new THREE.Vector3(-15, 0, -20),  // Serraglio Straight
      new THREE.Vector3(-25, 0, -15),  // Ascari Chicane entry
      new THREE.Vector3(-28, 0, -20),  
      new THREE.Vector3(-32, 0, -15),  // Ascari exit
      new THREE.Vector3(-38, 0, 0),    // Parabolica entry
      new THREE.Vector3(-35, 0, 15),   // Parabolica exit
    ]
  },
  spa: {
    name: "Spa-Francorchamps",
    location: "Stavelot, Belgium",
    lengthStr: "7.004 km",
    points: [
      new THREE.Vector3(-30, 0, 25),   // Start straight
      new THREE.Vector3(-15, 0, 25),   // La Source entry
      new THREE.Vector3(-11, 0, 27),   // La Source hairpin
      new THREE.Vector3(-12, 0, 20),   
      new THREE.Vector3(-22, -2.5, 5),   // Downhill to Eau Rouge
      new THREE.Vector3(-20, 2.0, -10),  // Eau Rouge
      new THREE.Vector3(-15, 7.5, -15),  // Raidillon uphill! (elevation change)
      new THREE.Vector3(5, 9.0, -25),   // Kemmel Straight uphill
      new THREE.Vector3(25, 8.0, -30),   // Les Combes chicane
      new THREE.Vector3(32, 6.0, -25),
      new THREE.Vector3(28, 4.0, -15),   // Malmedy / Rivage
      new THREE.Vector3(20, 1.5, -5),    // Bruxelles hairpin (downhill)
      new THREE.Vector3(12, 0, 5),     
      new THREE.Vector3(8, -2.0, 12),    // Double Gauche (Pouhon) downhill
      new THREE.Vector3(0, -2.5, 18),
      new THREE.Vector3(-10, -1.0, 15),  // Fagnes
      new THREE.Vector3(-18, 0.5, 8),    // Campus / Stavelot
      new THREE.Vector3(-28, 0, 15),   // Blanchimont
    ]
  },
  suzuka: {
    name: "Suzuka GP",
    location: "Suzuka, Japan",
    lengthStr: "5.807 km",
    points: [
      new THREE.Vector3(-30, 0, 20),   // Start straight
      new THREE.Vector3(-10, 0, 20),   // First Corner
      new THREE.Vector3(0, 0, 17),     // S-Curves
      new THREE.Vector3(10, 0, 11),
      new THREE.Vector3(5, 0, 1),
      new THREE.Vector3(12, 0, -6),
      new THREE.Vector3(18, 0, -16),   // Dunlop Curve
      new THREE.Vector3(12, 0, -26),   // Degner 1
      new THREE.Vector3(5, 0, -29),    // Degner 2
      new THREE.Vector3(-2, 0.0, -20),  // Underpass (Low level, Y = 0)
      new THREE.Vector3(-15, 0, -14),  // Hairpin
      new THREE.Vector3(-22, 0, -24),  
      new THREE.Vector3(-15, 0.5, -31),  // 200R
      new THREE.Vector3(0, 1.5, -34),    // Spoon Curve entry
      new THREE.Vector3(15, 2.5, -31),   // Spoon Curve double-left
      new THREE.Vector3(10, 4.5, -20),   // Spoon Curve exit uphill to bridge
      new THREE.Vector3(3, 5.5, -12),    // Heading to Bridge
      new THREE.Vector3(-2, 5.5, -20),   // OVERPASS / BRIDGE (High level, Y = 5.5 - crossing directly over underpass!)
      new THREE.Vector3(-8, 4.5, -25),   
      new THREE.Vector3(-18, 2.0, -15),  // Downhill from bridge
      new THREE.Vector3(-25, 0, 0),    // 130R left curve
      new THREE.Vector3(-35, 0, 10),   // Casio Triangle chicane
      new THREE.Vector3(-32, 0, 15),
    ]
  }
};

// Initialize everything on load
window.addEventListener('DOMContentLoaded', () => {
  init();
  initMiniatures();
  setupUIEventListeners();
  setupKeyboardControls();
});

function init() {
  const container = document.getElementById('canvas-container');
  const width = container.clientWidth;
  const height = container.clientHeight;
  
  // Scene - stark white background
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xffffff);
  
  // Add a very subtle grid on the floor to maintain technical depth
  const gridHelper = new THREE.GridHelper(100, 50, 0xdddddd, 0xf3f3f3);
  gridHelper.position.y = -0.05;
  scene.add(gridHelper);
  
  // Camera
  camera = new THREE.PerspectiveCamera(40, width / height, 1, 1000);
  camera.position.set(0, 50, 80);
  
  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  container.appendChild(renderer.domElement);
  
  // OrbitControls
  orbitControls = new THREE.OrbitControls(camera, renderer.domElement);
  orbitControls.enableDamping = true;
  orbitControls.dampingFactor = 0.05;
  orbitControls.maxPolarAngle = Math.PI / 2 - 0.02; // Don't go below floor
  orbitControls.minDistance = 5;
  orbitControls.maxDistance = 150;
  
  // Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
  scene.add(ambientLight);
  
  // Soft directional light for shadows
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.45);
  dirLight.position.set(20, 60, 20);
  dirLight.castShadow = true;
  dirLight.shadow.mapSize.width = 2048;
  dirLight.shadow.mapSize.height = 2048;
  dirLight.shadow.camera.near = 0.5;
  dirLight.shadow.camera.far = 150;
  
  const d = 50;
  dirLight.shadow.camera.left = -d;
  dirLight.shadow.camera.right = d;
  dirLight.shadow.camera.top = d;
  dirLight.shadow.camera.bottom = -d;
  dirLight.shadow.bias = -0.0005;
  scene.add(dirLight);
  
  // Load initial track
  loadTrack(simState.activeTrack);
  
  // Clock for updates
  clock = new THREE.Clock();
  
  // Start Render Loop
  animate();
  
  // Window Resize
  window.addEventListener('resize', onWindowResize);
}

// Render loop
function animate() {
  requestAnimationFrame(animate);
  
  const dt = Math.min(clock.getDelta(), 0.1); // Cap delta time to avoid physics explosion
  
  // Update Physics and controls
  updateSimulation(dt);
  
  // Update Camera based on modes
  updateCamera();
  
  // Update controls
  orbitControls.update();
  
  renderer.render(scene, camera);
}

function onWindowResize() {
  const container = document.getElementById('canvas-container');
  const width = container.clientWidth;
  const height = container.clientHeight;
  
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  
  renderer.setSize(width, height);
}

// Generate Track Spline & Mesh
function loadTrack(trackId) {
  // Show spinner
  const spinner = document.getElementById('loading-spinner');
  if (spinner) spinner.classList.add('active');
  
  activeTrackId = trackId;
  const config = tracksConfig[trackId];
  
  // Update HUD values
  document.getElementById('hud-track-name').textContent = config.name;
  document.getElementById('hud-track-length').textContent = config.lengthStr;
  
  // Create Spline Curve
  activeCurve = new THREE.CatmullRomCurve3(config.points, true);
  
  // Rebuild Track Mesh
  rebuildTrackMesh();
  
  // Spawn or reposition car
  setupCar();
  
  // Reset lap timing
  carState.closestT = 0;
  carState.lapStartTime = performance.now();
  carState.lapHalfway = false;
  carState.cteSum = 0;
  carState.cteCount = 0;
  carState.maxSpeedReached = 0;
  
  // Hide spinner after small delay
  setTimeout(() => {
    if (spinner) spinner.classList.remove('active');
  }, 250);
}

function rebuildTrackMesh() {
  // Remove existing meshes from scene
  if (mainTrackMesh) scene.remove(mainTrackMesh);
  if (mainLineMesh) scene.remove(mainLineMesh);
  if (mainCurbLMesh) scene.remove(mainCurbLMesh);
  if (mainCurbRMesh) scene.remove(mainCurbRMesh);
  if (startGridMesh) scene.remove(startGridMesh);
  
  const width = simState.trackWidth;
  // Resolution based on complexity slider (from 1 to 5, mapped to 80 - 350 segments)
  const segments = 60 + simState.complexity * 50;
  
  const positions = [];
  const normals = [];
  const uvs = [];
  const indices = [];
  
  const yellowPos = [];
  const yellowNorm = [];
  const yellowIndices = [];
  const yellowWidth = 0.08;
  
  const curbLeftPos = [];
  const curbLeftCol = [];
  const curbLeftNorm = [];
  const curbLeftIndices = [];
  
  const curbRightPos = [];
  const curbRightCol = [];
  const curbRightNorm = [];
  const curbRightIndices = [];
  const curbWidth = 0.26;
  
  // Generate vertices along the spline
  for (let i = 0; i <= segments; i++) {
    const t = i / segments;
    const p = activeCurve.getPointAt(t);
    const tangent = activeCurve.getTangentAt(t).normalize();
    const up = new THREE.Vector3(0, 1, 0);
    const side = new THREE.Vector3().crossVectors(tangent, up).normalize();
    const normal = new THREE.Vector3().crossVectors(side, tangent).normalize();
    
    // 1. Asphalt vertices
    const pLeft = p.clone().addScaledVector(side, -width / 2);
    const pRight = p.clone().addScaledVector(side, width / 2);
    
    positions.push(pLeft.x, pLeft.y, pLeft.z);
    positions.push(pRight.x, pRight.y, pRight.z);
    
    normals.push(normal.x, normal.y, normal.z);
    normals.push(normal.x, normal.y, normal.z);
    
    uvs.push(0, t * 15); // Repeat texture coordinates
    uvs.push(1, t * 15);
    
    // 2. Yellow centerline vertices (raised slightly to prevent z-fighting)
    const pCenter = p.clone().addScaledVector(normal, 0.005);
    const pLineLeft = pCenter.clone().addScaledVector(side, -yellowWidth / 2);
    const pLineRight = pCenter.clone().addScaledVector(side, yellowWidth / 2);
    
    yellowPos.push(pLineLeft.x, pLineLeft.y, pLineLeft.z);
    yellowPos.push(pLineRight.x, pLineRight.y, pLineRight.z);
    yellowNorm.push(normal.x, normal.y, normal.z);
    yellowNorm.push(normal.x, normal.y, normal.z);
    
    // 3. Curbs (Red and White alternating stripes)
    const stripeCount = Math.round(activeCurve.getLength() * 0.7);
    const isWhite = Math.floor(t * stripeCount) % 2 === 0;
    const curbColor = isWhite ? [1.0, 1.0, 1.0] : [0.88, 0.02, 0.0];
    
    // Left curb (slightly higher elevation)
    const pCurbLOuter = p.clone().addScaledVector(side, -width / 2 - curbWidth).addScaledVector(normal, 0.015);
    const pCurbLInner = p.clone().addScaledVector(side, -width / 2).addScaledVector(normal, 0.01);
    
    curbLeftPos.push(pCurbLOuter.x, pCurbLOuter.y, pCurbLOuter.z);
    curbLeftPos.push(pCurbLInner.x, pCurbLInner.y, pCurbLInner.z);
    curbLeftCol.push(...curbColor, ...curbColor);
    curbLeftNorm.push(normal.x, normal.y, normal.z);
    curbLeftNorm.push(normal.x, normal.y, normal.z);
    
    // Right curb
    const pCurbRInner = p.clone().addScaledVector(side, width / 2).addScaledVector(normal, 0.01);
    const pCurbROuter = p.clone().addScaledVector(side, width / 2 + curbWidth).addScaledVector(normal, 0.015);
    
    curbRightPos.push(pCurbRInner.x, pCurbRInner.y, pCurbRInner.z);
    curbRightPos.push(pCurbROuter.x, pCurbROuter.y, pCurbROuter.z);
    curbRightCol.push(...curbColor, ...curbColor);
    curbRightNorm.push(normal.x, normal.y, normal.z);
    curbRightNorm.push(normal.x, normal.y, normal.z);
  }
  
  // Generate faces (indices)
  for (let i = 0; i < segments; i++) {
    const a = i * 2;
    const b = i * 2 + 1;
    const c = (i + 1) * 2;
    const d = (i + 1) * 2 + 1;
    
    // Asphalt
    indices.push(a, c, b);
    indices.push(b, c, d);
    
    // Centerline
    yellowIndices.push(a, c, b);
    yellowIndices.push(b, c, d);
    
    // Curbs
    curbLeftIndices.push(a, c, b);
    curbLeftIndices.push(b, c, d);
    curbRightIndices.push(a, c, b);
    curbRightIndices.push(b, c, d);
  }
  
  // 1. Asphalt Mesh
  const asphaltGeom = new THREE.BufferGeometry();
  asphaltGeom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  asphaltGeom.setAttribute('normal', new THREE.Float32BufferAttribute(normals, 3));
  asphaltGeom.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  asphaltGeom.setIndex(indices);
  
  // Custom dark asphalt material with subtle roughness
  const asphaltMat = new THREE.MeshStandardMaterial({
    color: 0x242426,
    roughness: 0.85,
    metalness: 0.05,
    side: THREE.DoubleSide
  });
  mainTrackMesh = new THREE.Mesh(asphaltGeom, asphaltMat);
  mainTrackMesh.receiveShadow = true;
  scene.add(mainTrackMesh);
  
  // 2. Yellow centerline Mesh
  const centerlineGeom = new THREE.BufferGeometry();
  centerlineGeom.setAttribute('position', new THREE.Float32BufferAttribute(yellowPos, 3));
  centerlineGeom.setAttribute('normal', new THREE.Float32BufferAttribute(yellowNorm, 3));
  centerlineGeom.setIndex(yellowIndices);
  
  const yellowMat = new THREE.MeshBasicMaterial({
    color: 0xf2ca00,
    side: THREE.DoubleSide
  });
  mainLineMesh = new THREE.Mesh(centerlineGeom, yellowMat);
  scene.add(mainLineMesh);
  
  // 3. Curbs Meshes (using Vertex Colors)
  const curbLeftGeom = new THREE.BufferGeometry();
  curbLeftGeom.setAttribute('position', new THREE.Float32BufferAttribute(curbLeftPos, 3));
  curbLeftGeom.setAttribute('color', new THREE.Float32BufferAttribute(curbLeftCol, 3));
  curbLeftGeom.setAttribute('normal', new THREE.Float32BufferAttribute(curbLeftNorm, 3));
  curbLeftGeom.setIndex(curbLeftIndices);
  
  const curbRightGeom = new THREE.BufferGeometry();
  curbRightGeom.setAttribute('position', new THREE.Float32BufferAttribute(curbRightPos, 3));
  curbRightGeom.setAttribute('color', new THREE.Float32BufferAttribute(curbRightCol, 3));
  curbRightGeom.setAttribute('normal', new THREE.Float32BufferAttribute(curbRightNorm, 3));
  curbRightGeom.setIndex(curbRightIndices);
  
  const curbMat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.7,
    side: THREE.DoubleSide
  });
  
  mainCurbLMesh = new THREE.Mesh(curbLeftGeom, curbMat);
  mainCurbLMesh.castShadow = true;
  mainCurbLMesh.receiveShadow = true;
  scene.add(mainCurbLMesh);
  
  mainCurbRMesh = new THREE.Mesh(curbRightGeom, curbMat);
  mainCurbRMesh.castShadow = true;
  mainCurbRMesh.receiveShadow = true;
  scene.add(mainCurbRMesh);
  
  // 4. Start/Finish grid lines (simple decorative strips at t = 0)
  createStartGrid(width);
}

function createStartGrid(trackWidth) {
  const p0 = activeCurve.getPointAt(0);
  const tangent = activeCurve.getTangentAt(0).normalize();
  const up = new THREE.Vector3(0, 1, 0);
  const side = new THREE.Vector3().crossVectors(tangent, up).normalize();
  const normal = new THREE.Vector3().crossVectors(side, tangent).normalize();
  
  const startGridGeom = new THREE.PlaneGeometry(trackWidth, 0.4);
  const gridMat = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.8
  });
  
  startGridMesh = new THREE.Mesh(startGridGeom, gridMat);
  // Align to road surface direction
  startGridMesh.position.copy(p0).addScaledVector(normal, 0.008);
  startGridMesh.up.copy(normal);
  startGridMesh.lookAt(p0.clone().add(tangent));
  startGridMesh.rotateX(Math.PI / 2); // Make it coplanar to road surface
  scene.add(startGridMesh);
}

// Stylized F1 Car creation
function setupCar() {
  if (car) scene.remove(car);
  
  car = new THREE.Group();
  
  const bodyColor = 0xe10600; // Formula 1 Red
  const chassisMat = new THREE.MeshStandardMaterial({ color: bodyColor, roughness: 0.1, metalness: 0.8 });
  const wingMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.5, metalness: 0.2 }); // Matte carbon look
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x1a1a1a, roughness: 0.7 });
  const sensorMat = new THREE.MeshBasicMaterial({ color: 0x00ff88 }); // Green LED for sensor array
  
  // Main chassis
  const chassis = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.2, 1.8), chassisMat);
  chassis.position.y = 0.15;
  chassis.castShadow = true;
  chassis.receiveShadow = true;
  car.add(chassis);
  
  // Nose cone
  const nose = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.12, 0.7), chassisMat);
  nose.position.set(0, 0.11, 1.15);
  nose.castShadow = true;
  car.add(nose);
  
  // Front Wing
  const frontWing = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.04, 0.25), wingMat);
  frontWing.position.set(0, 0.06, 1.45);
  frontWing.castShadow = true;
  car.add(frontWing);
  
  // Rear Wing
  const rearWing = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.04, 0.25), wingMat);
  rearWing.position.set(0, 0.55, -0.85);
  rearWing.castShadow = true;
  car.add(rearWing);
  
  // Rear wing endplates
  const epL = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.4, 0.35), wingMat);
  epL.position.set(-0.65, 0.45, -0.85);
  const epR = epL.clone();
  epR.position.x = 0.65;
  car.add(epL);
  car.add(epR);
  
  // Support pillars for rear wing
  const pillarL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.4, 0.08), chassisMat);
  pillarL.position.set(-0.2, 0.3, -0.8);
  const pillarR = pillarL.clone();
  pillarR.position.x = 0.2;
  car.add(pillarL);
  car.add(pillarR);
  
  // Cockpit halo loop (stylized)
  const halo = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.03, 8, 24, Math.PI), wingMat);
  halo.position.set(0, 0.3, 0.2);
  halo.rotation.x = Math.PI / 2;
  car.add(halo);
  
  // Camera pod above engine cover
  const camPod = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.15), new THREE.MeshBasicMaterial({ color: 0xf2ca00 }));
  camPod.position.set(0, 0.52, -0.1);
  car.add(camPod);
  
  // Wheels
  const wheelGeom = new THREE.CylinderGeometry(0.26, 0.26, 0.32, 16);
  wheelGeom.rotateZ(Math.PI / 2); // Correct cylinder orientation
  
  const wheels = [];
  const wheelPositions = [
    { name: 'fl', x: -0.6, y: 0.26, z: 0.6 },
    { name: 'fr', x: 0.6, y: 0.26, z: 0.6 },
    { name: 'rl', x: -0.62, y: 0.26, z: -0.6 },
    { name: 'rr', x: 0.62, y: 0.26, z: -0.6 }
  ];
  
  wheelPositions.forEach(wp => {
    const wheelGroup = new THREE.Group();
    wheelGroup.position.set(wp.x, wp.y, wp.z);
    
    const wheelMesh = new THREE.Mesh(wheelGeom, wheelMat);
    wheelMesh.castShadow = true;
    wheelGroup.add(wheelMesh);
    
    // Wheel details (rims)
    const rimGeom = new THREE.CylinderGeometry(0.12, 0.12, 0.34, 8);
    rimGeom.rotateZ(Math.PI / 2);
    const rimMesh = new THREE.Mesh(rimGeom, new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 0.9 }));
    wheelGroup.add(rimMesh);
    
    car.add(wheelGroup);
    wheels.push(wheelGroup);
  });
  
  // Glow optical line-following sensor underneath front nose
  const sensorGlow = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.02, 0.05), sensorMat);
  sensorGlow.position.set(0, 0.04, 1.3);
  car.add(sensorGlow);
  
  // Save references for wheel animation
  car.userData = {
    wheels: wheels,
    flWheel: wheels[0],
    frWheel: wheels[1],
    sensorGlow: sensorGlow
  };
  
  scene.add(car);
  
  // Position car initially at start point
  resetCarPosition();
}

function resetCarPosition() {
  if (!car || !activeCurve) return;
  
  carState.closestT = 0;
  const p0 = activeCurve.getPointAt(0);
  const tangent = activeCurve.getTangentAt(0).normalize();
  const up = new THREE.Vector3(0, 1, 0);
  const side = new THREE.Vector3().crossVectors(tangent, up).normalize();
  const normal = new THREE.Vector3().crossVectors(side, tangent).normalize();
  
  carState.position.copy(p0).addScaledVector(normal, 0.02);
  carState.yaw = Math.atan2(tangent.x, tangent.z);
  carState.speed = 0;
  carState.steerAngle = 0;
  
  carState.prevSensorError = 0;
  carState.integralError = 0;
  
  car.position.copy(carState.position);
  car.up.copy(normal);
  car.lookAt(carState.position.clone().add(tangent));
  
  // Reset steering wheels orientation
  car.userData.flWheel.rotation.y = 0;
  car.userData.frWheel.rotation.y = 0;
}

// Main Physics & Line Following Update
function updateSimulation(dt) {
  if (!car || !activeCurve) return;
  
  const wheelbase = 1.8;
  const maxSteerLimit = 0.55; // ~32 degrees
  const acceleration = 12.0;  // m/s^2 acceleration
  const braking = 25.0;       // m/s^2 deceleration
  const trackLength = activeCurve.getLength();
  
  // 1. Locate closest parameter t on spline to current car position
  let bestT = carState.closestT;
  let minDist = Infinity;
  const searchRange = 0.06; // 6% window around current location
  const steps = 30;
  for (let i = -steps/2; i <= steps/2; i++) {
    const testT = (carState.closestT + (i / steps) * searchRange + 1.0) % 1.0;
    const pt = activeCurve.getPointAt(testT);
    const dist = carState.position.distanceTo(pt);
    if (dist < minDist) {
      minDist = dist;
      bestT = testT;
    }
  }
  
  // Handle lap crossing boundary
  const oldT = carState.closestT;
  carState.closestT = bestT;
  
  if (oldT > 0.5 && carState.closestT < 0.1) {
    carState.lapHalfway = true;
  }
  if (oldT > 0.8 && carState.closestT < 0.05 && carState.lapHalfway) {
    completeLap();
  }
  
  // Calculate local track frame of reference
  const pRef = activeCurve.getPointAt(carState.closestT);
  const tangent = activeCurve.getTangentAt(carState.closestT).normalize();
  const up = new THREE.Vector3(0, 1, 0);
  const side = new THREE.Vector3().crossVectors(tangent, up).normalize();
  const normal = new THREE.Vector3().crossVectors(side, tangent).normalize();
  
  // Compute Cross-Track Error (CTE)
  const toCar = carState.position.clone().sub(pRef);
  carState.cte = toCar.dot(side); // Signed lateral displacement
  
  // Average CTE logging
  carState.cteSum += Math.abs(carState.cte);
  carState.cteCount++;
  
  // Check for critical crash condition (car has flown completely off-road)
  const trackLimit = simState.trackWidth / 2 + 1.2;
  if (Math.abs(carState.cte) > trackLimit) {
    triggerOffTrackReset();
  }
  
  // Determine sensor preview coordinates
  // Position of sensor on car is extended forward along car's heading
  const headingVec = new THREE.Vector3(Math.sin(carState.yaw), 0, Math.cos(carState.yaw)).normalize();
  // Project sensor position onto 3D road normal slope
  const sensorPos = carState.position.clone().addScaledVector(headingVec, simState.sensorOffset);
  
  // Find track reference point ahead for line-following sensor
  const sensorT = (carState.closestT + simState.sensorOffset / trackLength) % 1.0;
  const pSensorRef = activeCurve.getPointAt(sensorT);
  const sideSensor = activeCurve.getTangentAt(sensorT).cross(up).normalize();
  const toSensor = sensorPos.clone().sub(pSensorRef);
  const sensorError = toSensor.dot(sideSensor); // Measured error by front sensor array
  
  let targetForwardSpeed = 0;
  
  // 2. Control Logic Selection
  if (simState.autonomous) {
    // A. Autonomous mode active: apply PID steering & Speed management
    
    // PID Controller math
    const pTerm = simState.kp * sensorError;
    
    // Avoid integral windup
    carState.integralError = Math.max(-5, Math.min(5, carState.integralError + sensorError * dt));
    const iTerm = simState.ki * carState.integralError;
    
    const dTerm = simState.kd * (sensorError - carState.prevSensorError) / dt;
    carState.prevSensorError = sensorError;
    
    carState.steerAngle = -(pTerm + iTerm + dTerm);
    carState.steerAngle = Math.max(-maxSteerLimit, Math.min(maxSteerLimit, carState.steerAngle));
    
    // Smart Speed Management: decelerate in sharp curves!
    // curvature is calculated by looking ahead
    const previewT1 = (carState.closestT + 0.01) % 1.0;
    const previewT2 = (carState.closestT + 0.03) % 1.0;
    const tan1 = activeCurve.getTangentAt(previewT1);
    const tan2 = activeCurve.getTangentAt(previewT2);
    const localCurvature = tan1.angleTo(tan2) * 5.0; // Radians change per distance unit
    
    // Scale target speed based on curvature: tighter corners = slower target
    const speedLimitCoeff = Math.max(0.35, 1.0 - localCurvature * 2.5);
    const speedSliderValue = simState.targetSpeed / 3.6; // Convert km/h to units/sec
    targetForwardSpeed = speedSliderValue * speedLimitCoeff;
    
  } else {
    // B. Manual Mode: Drive using arrow keys or WASD
    
    // Steering
    const steerRate = 2.0; // steering speed
    if (carState.keys.left) {
      carState.steerAngle = Math.min(maxSteerLimit, carState.steerAngle + steerRate * dt);
    } else if (carState.keys.right) {
      carState.steerAngle = Math.max(-maxSteerLimit, carState.steerAngle - steerRate * dt);
    } else {
      // Auto center
      if (carState.steerAngle > 0.02) carState.steerAngle -= steerRate * dt;
      else if (carState.steerAngle < -0.02) carState.steerAngle += steerRate * dt;
      else carState.steerAngle = 0;
    }
    
    // Throttle / Brake
    const speedSliderValue = simState.targetSpeed / 3.6;
    if (carState.keys.forward) {
      targetForwardSpeed = speedSliderValue;
    } else if (carState.keys.backward) {
      targetForwardSpeed = -speedSliderValue * 0.4; // Reverse is slower
    } else {
      targetForwardSpeed = 0; // Coasting
    }
  }
  
  // 3. Physical State Updates
  // Speed acceleration/deceleration kinematics
  const speedDiff = targetForwardSpeed - carState.speed;
  let throttleInput = 0;
  let brakeInput = 0;
  
  if (speedDiff > 0.1) {
    // Accelerate
    carState.speed = Math.min(targetForwardSpeed, carState.speed + acceleration * dt);
    throttleInput = Math.min(1.0, speedDiff / 10);
    brakeInput = 0;
  } else if (speedDiff < -0.1) {
    // Brake
    carState.speed = Math.max(targetForwardSpeed, carState.speed - braking * dt);
    throttleInput = 0;
    brakeInput = Math.min(1.0, -speedDiff / 15);
  } else {
    throttleInput = targetForwardSpeed > 0 ? 0.2 : 0;
    brakeInput = 0;
  }
  
  // Apply update to position and yaw using bicycle model kinematics
  carState.yaw += (carState.speed * Math.sin(carState.steerAngle) / wheelbase) * dt;
  carState.position.x += carState.speed * Math.sin(carState.yaw) * dt;
  carState.position.z += carState.speed * Math.cos(carState.yaw) * dt;
  
  // Project height directly to the track's spline height at this progress
  carState.position.y = pRef.y + normal.y * 0.025; // Sit on wheels
  
  // 4. Update F1 Car 3D Mesh Position and Orientation
  car.position.copy(carState.position);
  
  // Align car's up vector with local track normal (banking)
  car.up.copy(normal);
  
  // Aim front of the car along the combined heading vector
  const lookTarget = carState.position.clone().add(headingVec);
  car.lookAt(lookTarget);
  
  // Animate spinning wheels based on linear speed
  const wheelCircumference = 2 * Math.PI * 0.26;
  const wheelRotationAngle = (carState.speed * dt) / 0.26;
  car.userData.wheels.forEach(wheel => {
    // Rotate wheels around their local axle (X axis)
    wheel.children[0].rotation.x += wheelRotationAngle;
  });
  
  // Steer front wheels visual representation
  car.userData.flWheel.rotation.y = carState.steerAngle * 1.3;
  car.userData.frWheel.rotation.y = carState.steerAngle * 1.3;
  
  // 5. Update Telemetry displays
  updateTelemetryUI(throttleInput, brakeInput);
}

// Handle lap completion records
function completeLap() {
  carState.lapHalfway = false;
  carState.lapCount++;
  
  const now = performance.now();
  const lapTimeMs = now - carState.lapStartTime;
  carState.lapStartTime = now;
  
  const lapTimeSec = lapTimeMs / 1000;
  const avgCte = carState.cteCount > 0 ? (carState.cteSum / carState.cteCount) : 0;
  
  // Check if best lap
  let isBest = false;
  if (lapTimeSec < carState.bestLapTime) {
    carState.bestLapTime = lapTimeSec;
    isBest = true;
  }
  
  // Format time (MM:SS.hh)
  const formatTime = (tSec) => {
    const m = Math.floor(tSec / 60);
    const s = Math.floor(tSec % 60);
    const ms = Math.floor((tSec % 1) * 100);
    return `${m}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(2, '0')}`;
  };
  
  // Add to table
  const tbody = document.getElementById('lap-records-body');
  const emptyRow = tbody.querySelector('.empty-row');
  if (emptyRow) emptyRow.remove();
  
  const tr = document.createElement('tr');
  if (isBest) tr.classList.add('best-lap-row');
  tr.innerHTML = `
    <td>Lap ${carState.lapCount}</td>
    <td class="font-mono">${formatTime(lapTimeSec)} ${isBest ? '⭐' : ''}</td>
    <td>${Math.round(carState.maxSpeedReached * 3.6)} km/h</td>
    <td>${avgCte.toFixed(3)}m</td>
  `;
  
  // Insert at top
  tbody.insertBefore(tr, tbody.firstChild);
  
  // Reset logs
  carState.cteSum = 0;
  carState.cteCount = 0;
  carState.maxSpeedReached = 0;
}

// Fallback recovery if car crashes out
function triggerOffTrackReset() {
  const statusDisplay = document.getElementById('status-display');
  const statusDot = document.querySelector('.status-dot');
  
  if (statusDisplay) {
    statusDisplay.textContent = "SIMULATOR: OFF-TRACK RECOVERY";
    statusDisplay.classList.add('f1-red-text');
  }
  if (statusDot) {
    statusDot.style.backgroundColor = "var(--f1-red)";
  }
  
  // Bring speed to zero and place back on track
  carState.speed = 0;
  
  setTimeout(() => {
    resetCarPosition();
    if (statusDisplay) {
      statusDisplay.textContent = "SIMULATOR: ACTIVE";
      statusDisplay.classList.remove('f1-red-text');
    }
    if (statusDot) {
      statusDot.style.backgroundColor = "var(--green-throttle)";
    }
  }, 1000);
}

// Telemetry visualizer & graphs
function updateTelemetryUI(throttle, brake) {
  // Speed in km/h
  const speedKmh = carState.speed * 3.6;
  if (speedKmh > carState.maxSpeedReached) {
    carState.maxSpeedReached = carState.speed;
  }
  
  // Update numerical telemetry texts
  document.getElementById('tel-speed').innerHTML = `${speedKmh.toFixed(1)} <span class="unit">km/h</span>`;
  document.getElementById('tel-cte').innerHTML = `${carState.cte.toFixed(3)} <span class="unit">m</span>`;
  document.getElementById('tel-steer').textContent = `${(carState.steerAngle * (180 / Math.PI)).toFixed(1)}°`;
  
  // Lap elapsed timer
  const elapsed = (performance.now() - carState.lapStartTime) / 1000;
  const m = Math.floor(elapsed / 60);
  const s = Math.floor(elapsed % 60);
  const ms = Math.floor((elapsed % 1) * 100);
  document.getElementById('tel-time').textContent = `${m}:${s.toString().padStart(2, '0')}.${ms.toString().padStart(2, '0')}`;
  
  // Update gauges on HUD
  // Steer steering wheel gauge (-32deg to +32deg mapped to 0% - 100%)
  const steerPercent = ((carState.steerAngle / 0.55) + 1) * 50; // Map -1..1 to 0..100
  document.getElementById('steer-gauge').style.width = `${Math.max(0, Math.min(100, steerPercent))}%`;
  document.getElementById('throttle-gauge').style.width = `${throttle * 100}%`;
  document.getElementById('brake-gauge').style.width = `${brake * 100}%`;
  
  // Add to SVG History graph (only add every 3 frames to keep smooth)
  if (Math.random() < 0.35) {
    cteHistory.push(carState.cte);
    if (cteHistory.length > maxCteHistoryLength) {
      cteHistory.shift();
    }
    
    // Draw SVG Line Path
    const svgPath = document.getElementById('cte-path');
    if (svgPath) {
      const width = 250;
      const height = 80;
      const centerY = height / 2;
      const scaleLimit = 1.6; // Max CTE visual bound
      
      let pathString = "";
      for (let i = 0; i < cteHistory.length; i++) {
        const x = (i / (maxCteHistoryLength - 1)) * width;
        const mappedCte = Math.max(-1, Math.min(1, cteHistory[i] / scaleLimit));
        const y = centerY - mappedCte * (height / 2 - 8);
        
        if (i === 0) pathString += `M ${x} ${y} `;
        else pathString += `L ${x} ${y} `;
      }
      svgPath.setAttribute('d', pathString);
    }
  }
}

// Camera Modes
function updateCamera() {
  if (!car) return;
  
  const relativeCameraOffset = new THREE.Vector3();
  const headingVec = new THREE.Vector3(Math.sin(carState.yaw), 0, Math.cos(carState.yaw)).normalize();
  const upNormal = new THREE.Vector3(0, 1, 0);
  
  // Get curve geometry normal to orient cameras
  if (activeCurve) {
    const ptTangent = activeCurve.getTangentAt(carState.closestT).normalize();
    const sideVec = new THREE.Vector3().crossVectors(ptTangent, upNormal).normalize();
    upNormal.crossVectors(sideVec, ptTangent).normalize();
  }
  
  switch (simState.cameraMode) {
    case 'top':
      // Stark top down flat projection
      camera.position.set(car.position.x, car.position.y + 35, car.position.z);
      camera.lookAt(car.position);
      orbitControls.target.copy(car.position);
      break;
      
    case 'chase':
      // Drag behind vehicle
      relativeCameraOffset.set(0, 2.2, -5.0); // Behind and above
      const chaseOffset = relativeCameraOffset.applyMatrix4(car.matrixWorld);
      camera.position.copy(chaseOffset);
      camera.lookAt(car.position.clone().addScaledVector(headingVec, 4));
      orbitControls.target.copy(car.position);
      break;
      
    case 'driver':
      // Cockpit perspective
      relativeCameraOffset.set(0, 0.42, -0.05); // Eye level in cockpit
      const driverOffset = relativeCameraOffset.applyMatrix4(car.matrixWorld);
      camera.position.copy(driverOffset);
      
      // Look forward along heading with subtle normal tilt
      const lookDir = car.position.clone().addScaledVector(headingVec, 10);
      camera.lookAt(lookDir);
      orbitControls.target.copy(lookDir);
      break;
      
    case 'orbital':
    default:
      // Focus orbit control target on the car so camera pans with vehicle motion
      orbitControls.target.copy(car.position);
      break;
  }
}

// Set UI Control Event Listeners
function setupUIEventListeners() {
  // Tabs Switcher
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Deactivate all
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      
      // Activate clicked
      tab.classList.add('active');
      const panelId = `panel-${tab.dataset.tab}`;
      document.getElementById(panelId).classList.add('active');
    });
  });
  
  // Track Select Dropdown
  const select = document.getElementById('track-select');
  select.addEventListener('change', (e) => {
    const trackId = e.target.value;
    selectTrack(trackId);
  });
  
  // Track Width Slider
  const widthSlider = document.getElementById('slider-width');
  const widthVal = document.getElementById('width-val');
  widthSlider.addEventListener('input', (e) => {
    const width = parseFloat(e.target.value);
    simState.trackWidth = width;
    widthVal.textContent = `${width.toFixed(1)}m`;
    rebuildTrackMesh();
  });
  
  // Track Complexity Slider
  const compSlider = document.getElementById('slider-complexity');
  const compVal = document.getElementById('complexity-val');
  const compLabels = ["Low-Poly", "Draft", "Medium", "High", "Ultra-Smooth"];
  compSlider.addEventListener('input', (e) => {
    const val = parseInt(e.target.value);
    simState.complexity = val;
    compVal.textContent = compLabels[val - 1];
    rebuildTrackMesh();
  });
  
  // Speed Slider
  const speedSlider = document.getElementById('slider-speed');
  const speedVal = document.getElementById('speed-val');
  speedSlider.addEventListener('input', (e) => {
    const speed = parseInt(e.target.value);
    simState.targetSpeed = speed;
    speedVal.textContent = `${speed} km/h`;
  });
  
  // Autonomous Drive toggle
  const driveToggle = document.getElementById('toggle-drive');
  driveToggle.addEventListener('change', (e) => {
    simState.autonomous = e.target.checked;
    
    // Reset PID states
    carState.prevSensorError = 0;
    carState.integralError = 0;
  });
  
  // Reset Simulation Button
  document.getElementById('btn-reset').addEventListener('click', () => {
    resetCarPosition();
  });
  
  // Clear Laps records
  document.getElementById('btn-telemetry-clear').addEventListener('click', () => {
    document.getElementById('lap-records-body').innerHTML = `
      <tr class="empty-row"><td colspan="4">No lap data recorded yet</td></tr>
    `;
    carState.lapCount = 0;
    carState.bestLapTime = Infinity;
  });
  
  // PID tuning parameters inputs
  const kpSlider = document.getElementById('pid-kp');
  const kpVal = document.getElementById('pid-kp-val');
  kpSlider.addEventListener('input', (e) => {
    simState.kp = parseFloat(e.target.value);
    kpVal.textContent = simState.kp.toFixed(1);
  });
  
  const kiSlider = document.getElementById('pid-ki');
  const kiVal = document.getElementById('pid-ki-val');
  kiSlider.addEventListener('input', (e) => {
    simState.ki = parseFloat(e.target.value);
    kiVal.textContent = simState.ki.toFixed(2);
  });
  
  const kdSlider = document.getElementById('pid-kd');
  const kdVal = document.getElementById('pid-kd-val');
  kdSlider.addEventListener('input', (e) => {
    simState.kd = parseFloat(e.target.value);
    kdVal.textContent = simState.kd.toFixed(1);
  });
  
  const previewSlider = document.getElementById('sensor-offset');
  const previewVal = document.getElementById('sensor-offset-val');
  previewSlider.addEventListener('input', (e) => {
    simState.sensorOffset = parseFloat(e.target.value);
    previewVal.textContent = `${simState.sensorOffset.toFixed(1)}m`;
  });
  
  // Apply PID balanced preset button
  document.getElementById('btn-pid-preset').addEventListener('click', () => {
    kpSlider.value = 3.5;
    simState.kp = 3.5;
    kpVal.textContent = "3.5";
    
    kiSlider.value = 0.05;
    simState.ki = 0.05;
    kiVal.textContent = "0.05";
    
    kdSlider.value = 1.2;
    simState.kd = 1.2;
    kdVal.textContent = "1.2";
    
    previewSlider.value = 1.5;
    simState.sensorOffset = 1.5;
    previewVal.textContent = "1.5m";
  });
  
  // Camera HUD controls
  const camBtns = document.querySelectorAll('.cam-btn');
  camBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      camBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      simState.cameraMode = btn.dataset.cam;
      
      // If switching back to orbital, set camera to standard viewpoint
      if (simState.cameraMode === 'orbital') {
        camera.position.set(car.position.x, car.position.y + 20, car.position.z + 45);
        orbitControls.target.copy(car.position);
      }
    });
  });
  
  // Grid miniature cards interaction
  const cards = document.querySelectorAll('.track-card');
  cards.forEach(card => {
    card.addEventListener('click', () => {
      const trackId = card.dataset.track;
      selectTrack(trackId);
    });
  });
}

function selectTrack(trackId) {
  // Update dropdown select
  document.getElementById('track-select').value = trackId;
  
  // Update cards active states
  const cards = document.querySelectorAll('.track-card');
  cards.forEach(card => {
    if (card.dataset.track === trackId) {
      card.classList.add('active');
      card.querySelector('.card-action').textContent = "Active";
    } else {
      card.classList.remove('active');
      card.querySelector('.card-action').textContent = "Load Track";
    }
  });
  
  // Trigger simulation track transition
  loadTrack(trackId);
}

// Manual Keyboard controls WASD / Arrow Keys
function setupKeyboardControls() {
  window.addEventListener('keydown', (e) => {
    switch (e.key) {
      case 'ArrowUp':
      case 'w':
      case 'W':
        carState.keys.forward = true;
        break;
      case 'ArrowDown':
      case 's':
      case 'S':
        carState.keys.backward = true;
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        carState.keys.left = true;
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        carState.keys.right = true;
        break;
    }
  });
  
  window.addEventListener('keyup', (e) => {
    switch (e.key) {
      case 'ArrowUp':
      case 'w':
      case 'W':
        carState.keys.forward = false;
        break;
      case 'ArrowDown':
      case 's':
      case 'S':
        carState.keys.backward = false;
        break;
      case 'ArrowLeft':
      case 'a':
      case 'A':
        carState.keys.left = false;
        break;
      case 'ArrowRight':
      case 'd':
      case 'D':
        carState.keys.right = false;
        break;
    }
  });
}

// Create isolated 3D rotating canvas renderers for track mini cards
function initMiniatures() {
  const tracks = ['monaco', 'monza', 'spa', 'suzuka'];
  
  tracks.forEach(trackId => {
    const container = document.getElementById(`mini-${trackId}`);
    if (!container) return;
    
    const width = container.clientWidth || 220;
    const height = container.clientHeight || 120;
    
    // Scene Setup
    const miniScene = new THREE.Scene();
    miniScene.background = new THREE.Color(0xfafafa);
    
    // Camera
    const miniCamera = new THREE.PerspectiveCamera(45, width / height, 1, 150);
    miniCamera.position.set(0, 32, 45);
    miniCamera.lookAt(0, 0, 0);
    
    // WebGL Renderer
    const miniRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    miniRenderer.setSize(width, height);
    miniRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    container.appendChild(miniRenderer.domElement);
    
    // Lighting
    const ambient = new THREE.AmbientLight(0xffffff, 0.85);
    miniScene.add(ambient);
    const dir = new THREE.DirectionalLight(0xffffff, 0.35);
    dir.position.set(10, 20, 10);
    miniScene.add(dir);
    
    // Create track spline curve
    const config = tracksConfig[trackId];
    const miniCurve = new THREE.CatmullRomCurve3(config.points, true);
    
    // Render track as a clean 3D tube outline
    const tubeGeom = new THREE.TubeGeometry(miniCurve, 60, 0.45, 8, true);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0x555558,
      roughness: 0.5,
      metalness: 0.1
    });
    
    const tubeMesh = new THREE.Mesh(tubeGeom, tubeMat);
    miniScene.add(tubeMesh);
    
    // Scale down track mesh to fit the small viewport
    // Different scale adjustments to ensure tracks sit perfectly centered
    const scaleFactor = trackId === 'monza' ? 0.38 : 0.42;
    tubeMesh.scale.set(scaleFactor, scaleFactor, scaleFactor);
    
    if (trackId === 'spa') {
      tubeMesh.position.y = -3; // Adjust for height changes
    } else if (trackId === 'suzuka') {
      tubeMesh.position.y = -1;
    }
    
    // Render loop for miniature canvases
    function animateMini() {
      requestAnimationFrame(animateMini);
      
      // Rotate track slowly for dynamic visualization
      tubeMesh.rotation.y += 0.007;
      
      miniRenderer.render(miniScene, miniCamera);
    }
    
    animateMini();
  });
}
