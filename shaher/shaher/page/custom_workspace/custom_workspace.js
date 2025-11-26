frappe.pages['custom-workspace'].on_page_load = function(wrapper) {
    frappe.require([
        "https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js",
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.25/jspdf.plugin.autotable.min.js"
    ], function() {
        console.log("External libraries loaded!");
    });

    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Custom Workspace',
        single_column: true
    });

    // ✅ Set breadcrumb properly
    frappe.breadcrumbs.add("Home", "Custom Workspace");


  
  window.toggleUpdates = function() {
    const updatesWrapper = document.getElementById('latest-updates-wrapper');
    const container = document.getElementById("latest-updates-list");
    if (updatesWrapper.style.display === 'none' || updatesWrapper.style.display === '') {
      updatesWrapper.style.display = 'block';
      container.style.display = 'block';  // Show the updates section
    } else {
      updatesWrapper.style.display = 'none'; 
      container.style.display = 'none'; // Hide the updates section
    }
    if (updatesWrapper.classList.contains("show")) {
  updatesWrapper.classList.remove("show");
  setTimeout(() => updatesWrapper.style.display = "none", 300);
} else {
  updatesWrapper.style.display = "block";
  setTimeout(() => updatesWrapper.classList.add("show"), 10);
}

  };
	const style = document.createElement('style');
  style.innerHTML = `
 body {
  margin: 0;
  padding: 0;
}
.teampro-container {bottom: 0px; 
  right: 0px;  padding:0px; width: 100%; font-family: Arial, sans-serif; display: flex; flex-direction: column; }
body {
  margin: 0;
  padding: 0;
}

/* Announcement Box */
.announcement-box {
  position: fixed;
  right: 5px;
  width: 40px;
  height: 40px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 999; 
  
}
#latest-updates-list {
  flex: 1;
  padding: 10px;
}
.announcement-box .announcement-icon {
  font-size: 30px;
  color: red;
}
.latest-updates-wrapper {
  background: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: fixed; 
  bottom: 0;
  right: 20px;
  width: 400px;
  max-height: 700px; 
  display: none;
  z-index: 10;

  display: flex;
  flex-direction: column;
   overflow-y: auto; 
}

/* Header fixed */
.updates-header {
  background: #f4f4f4;
  padding: 10px 15px;
  margin: 0;
  border-bottom: 1px solid #ddd;
  flex-shrink: 0; /* prevent shrinking */
  position: sticky;
  top: 0;
  z-index: 11;
}

/* Scrollable announcements */
.updates-list {
  flex: 1; /* take all available space */
  overflow-y: auto; 
  padding: 10px;
}

/* Cards */
.update-card {
  background: #f8ecff;
  border-left: 4px solid #c084fc;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  color: #333;
  margin-bottom: 10px; 
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.update-card:hover {
  transform: translateY(-2px);
}

.update-date {
  font-size: 12px;
  color: #888;
  font-weight: bold;
  margin-bottom: 4px;
}

.update-content {
  font-size: 14px;
  line-height: 1.4;
}


@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}


.full-width-page .page-head, .full-width-page .page-actions { display: none; }
.full-width-page .layout-main-section { padding: 0 !important; }
      
.theme-morning {
  background-color: #f2fbff;
}

.theme-afternoon {
  background-color: #f2fbff;
}

.theme-evening {
  background-color: #f2fbff;
}

.theme-night {
  background-color: #f2fbff;
  color: black;
}


.toggle-buttons {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 5;
  display: inline-flex;
  border: 1px solid #cfd9e3;
  border-radius: 999px;
  overflow: none;
  background-color: #f9fafc;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.toggle-buttons button {
  border: none;
  background: none;
  padding: 8px 20px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  transition: all 0.3s ease;
}

.toggle-buttons button.active {
  background-color: #e6f0ff;
  color: #1a73e8;
  font-weight: 500;
}

.greeting {
  display: flex;
  align-items: center;
  gap: -10px;
  background-image: linear-gradient(to right, #dceeff, #f0f8ff);
}

.greeting h2 { margin: 0; font-size: 26px; font-weight: 600; }
.greeting p { margin: 5px 0 0; font-size: 15px; }
#teampro-image {
  height: 220px;
  width: 100%;
  object-fit: cover;

}


.sunrise-container { 
  position: relative; 
  height: 100px; 
  overflow: hidden;
  margin-bottom: 0;
  }
.cloudPane { 
  position: relative; 
  width: 100%; 
  height: 100%; 
  padding-bottom: 0 !important;
  margin-bottom: 0 !important;
  }

.cloudPane.morning { background: linear-gradient(to top, #a5e5ff, #a5e5ff); }
.cloudPane.afternoon { background: #bcdaed; }
.cloudPane.evening { background: #ed8639; }
.cloudPane.night { background: #021f31; }

.sun, {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  position: absolute;
  bottom: 20px;
  right: 30px;
  z-index: 2;
  opacity: 0.85;
}

.sun { background: radial-gradient(circle, #FFD700 60%, #FFA500 100%); }
.sun.bright { background: radial-gradient(circle, #FFF176 40%, #FFD54F 100%); }
.sun.set { background: radial-gradient(circle, #FFB74D 40%, #FF9800 100%); }
.moon-half {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  transform: translate(-50%, -50%);
  background-color: white;
  border-radius: 50%;
  overflow: hidden;
}modal-lg {
  max-width: 1000px !important; /* adjust as needed */
} 

.moon-half::before {
  content: '';
  position: absolute;
  width: 100px;
  height: 100px;
  background: black;
  border-radius: 50%;
  left: 25px; /* shift creates crescent */
  top: 0;
}





.stars { position: absolute; width: 100%; height: 100%; top: 0; left: 0; z-index: 1; }
.star {
  width: 3px;
  height: 3px;
  background: white;
  position: absolute;
  border-radius: 50%;
  animation: twinkle 2s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.3); }
}

.cloud {
  width: 200px;
  height: 60px;
  background: #fff;
  border-radius: 100px;
  position: absolute;
  opacity: 0.6;
}

.cloud:before, .cloud:after {
  content: '';
  position: absolute;
  background: #fff;
  border-radius: 100px;
}

.cloud:before { width: 100px; height: 80px; top: -15px; left: 10px; }
.cloud:after { width: 120px; height: 120px; top: -45px; right: 15px; }

.x1 { top: 20px; left: -200px; animation: moveclouds-right 30s linear infinite; }
.x2 { top: 60px; left: -250px; animation: moveclouds-right 40s linear infinite; }
.x3 { top: 100px; left: -300px; animation: moveclouds-right 35s linear infinite; }
.x4 { top: 140px; left: -180px; animation: moveclouds-right 25s linear infinite; }
.x5 { top: 30px; left: -220px; animation: moveclouds-right 38s linear infinite; }

@keyframes moveclouds-right {
  0% { transform: translateX(0); }
  100% { transform: translateX(1500px); }
}

.main-container { padding: 20px 10px; background-color: #eaf4ff;margin-top: -60px }
.section-title { font-weight: bold; font-size: 16px; margin: 20px 0 10px; }
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.fav_card {
  background-color: white;
  padding: 16px;
  width: 150px;
  height: 180px; 
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: all 0.3s ease;
  flex-direction: column;
}
.fav_card {
  transition: all 0.3s ease;
}



.fav_card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}


.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.card {
  background-color: white;
  padding: 16px;
  width: 150px;
  height: 180px; 
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: all 0.3s ease;
  flex-direction: column;
}
  .card {
    transition: all 0.3s ease;
  }

.card-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card.red { background-color: #fff0dd; }


@keyframes slideInFade {
  0% {
    transform: translateY(10px);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}.moon-crescent {
  width: 80px;
  height: 80px;
  background: #d0d0d0;
  border-radius: 50%;
  position: absolute;
  top: 20px;
  right: 30px;
  z-index: 2;
}

.moon-crescent::before {
  content: '';
  position: absolute;
  width: 80px;
  height: 80px;
  background: #021f31; 
  border-radius: 50%;
  left: 20px; 
  top: 0;
}

.greeting-overlay {
  position: relative;
  width: 100%;
  height: 260px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.greeting-overlay img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.92;
}

.greeting-text {
  position: absolute;
  top: 50%;
  left: 8%;
  transform: translateY(-50%);
  color: #fff;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

.greeting-text h2 {
  font-size: 28px;
  margin: 0;
  font-weight: bold;
}

.greeting-text p {
  font-size: 16px;
  margin: 8px 0 0;
}

.celebrations-wrapper {
  display: flex;
  gap: 20px;
  flex-wrap: nowrap;        
  justify-content: center;  
  align-items: stretch;    
  width: 100%;
  overflow-x: auto;      
  padding: 10px 0;
}


 .birthday-card-container {
  flex: 1 1 820px;
  width: 100%;
  background: #fff0dd;
  padding: 20px;
  max-width: 450px;
  margin-left:20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  position: relative;
}
  .celebration-card {
  flex: 1 1 300px;
  width: 450px;
  height: 450px;
  background: #fff0dd;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.celebration-card .profile-pic {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  margin-bottom: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.celebration-card .message {
  margin: 8px 0 4px;
  font-size: 16px;
  font-weight: 500;
}

.celebration-card .designation {
  font-size: 14px;
  color: #555;
  margin-bottom: 6px;
}

.celebration-card .emoji {
  font-size: 22px;
  margin: 12px 0;
}

.celebration-card .send-wish-btn {
  background: #e6f7ff;
  border: none;
  border-radius: 20px;
  padding: 6px 12px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.celebration-card .send-wish-btn:hover {
  background: #bae7ff;
}

.nav-btn {
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  color: #bae7ff;
  font-size: 18px;
  cursor: pointer;
}
.nav-btn:hover { color: #bae7ff; }
.joiner-prev { left: 5px; }
.joiner-next { right: 5px; }
.birthday-prev { left: 5px; }

.birthday-next{ right: 5px; }
.anniversary-prev { left: 5px; }
.anniversary-next { right: 5px; }
.celebration-box {
  width: 320px;
  min-height: 300px;
  background: #e6f7ff; 
  text-align: center;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.employee-name {
  font-size: 20px;
  font-weight: bold;
  margin-top: 10px;
}

.birthday-wish {
  font-size: 16px;
  font-style: italic;
  margin: 8px 0 16px;
  color: #444;
}

.send-wish-btn {
  background: #e6f7ff;
  padding: 10px 18px;
  font-size: 14px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.3s;
}
.send-wish-btn:hover {
  background: #e6f7ff;
}
  `;
  
  document.head.appendChild(style);
  const cloudsHTML = `
  <div class="cloud x1"></div>
  <div class="cloud x2"></div>
  <div class="cloud x3"></div>
  <div class="cloud x4"></div>
  <div class="cloud x5"></div>
`;
const starsHTML = `<div class="stars">${
  Array.from({ length: 12 }).map(() => {
    const top = Math.floor(Math.random() * 90);
    const left = Math.floor(Math.random() * 90);
    const delay = (Math.random() * 2).toFixed(2);
    return `<div class="star" style="top:${top}%;left:${left}%;animation-delay:${delay}s;"></div>`;
  }).join('')
}</div>`;



  $(wrapper).html(`
  <div class="cloud x1"></div>
  <div class="cloud x2"></div>
  <div class="cloud x3"></div>
  <div class="cloud x4"></div>
  <div class="cloud x5"></div>
	<div class="teampro-container">
    
  <div class="announcement-box" onclick="toggleUpdates()">
  <span class="announcement-icon">📢</span>
</div>

<div class="latest-updates-wrapper" id="latest-updates-wrapper" style="display: none;">
  <h3 class="updates-header" style="display: flex; align-items: center;">
    Latest Updates
    <span class="close-updates" title="Close" style="cursor: pointer; margin-left: auto;">✖</span>
  </h3>
  <div id="latest-updates-list" class="updates-list"></div>
</div>



  <div class="sunrise-container" id="sunrise-area"></div>
  <div class="greeting">
    <div class="greeting-overlay">
    <img id="teampro-image" src="" alt="Teampro Banner" />
    <div class="greeting-text">
      <h2 id="greeting-title" style="color:white;">Good Morning,</h2>
      <p id="greeting-desc">Let's do great things together. 🌟</p>
    </div>
  </div>

  </div>
  <div class="main-container">
  <div class="section-title" style="color:black">My Favourites</div>
 
  <div class="cards" id="fav-cards" style="display: flex; flex-wrap: wrap; gap: 16px;">
    <div class="card-wrapper">
      <div class="card" id="open-favourites" style="width: 30px; background-color: #87cefa; cursor:pointer;">
        ➕
      </div>
    </div>
  </div>
</div>


<div id="favourites-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); align-items:center; justify-content:center;">
  <div style="background:#fff; padding:20px; border-radius:12px; width:500px; max-height:80%; overflow:auto; position:relative;">
    <button id="close-modal" style="position:absolute; top:10px; right:10px;">X</button>
    <h3>Manage Favourites</h3>
    <div id="favourites-list" style="display:flex; flex-wrap:wrap; gap:10px;"></div>
  </div>
</div>
</div>
<div class="section-title">🎉 Today Celebrations </div>
</div>
  <div style="display: flex; flex-wrap: wrap; gap: 0px; justify-content: center; background-color:#e6f7ff;">
  <div class="celebrations-wrapper">
  <div id="birthday-display"></div>
  <div id="anniversary-display"></div>
  <div id="joiners-display"></div>
</div>


    </div>
  `);
  loadFavouriteCards()
  
  const birthdayMessages = [
  "🎉 Wishing you a day filled with happiness and a year filled with joy!",
  "🎂 Happy Birthday! May your dreams come true today and always.",
  "🎈 Hope your birthday is as special as you are!",
  "🥳 Have a fantastic birthday and a wonderful year ahead!",
  "😊 Sending you smiles for every moment of your special day!",
  "🎁 Stay awesome and keep shining bright. Happy Birthday!",
  "🌟 On your birthday, may your spirit be enriched in light, love, and hope.",
  "🎊 Cheers to you and your big day! May it be unforgettable!",
  "🌸 Enjoy your day to the fullest and don’t forget to smile!",
  "🎆 Another year older, wiser, and more amazing. Happy Birthday!"
];
const joinerMessages = [
  "🎉 Welcome aboard! Wishing you a successful journey with us.",
  "🙌 We’re thrilled to have you join our team!",
  "🎊 Congratulations on joining! Let's achieve great things together.",
  "🌟 Welcome to the family! Excited to work with you.",
  "👋 A warm welcome and best wishes on your new role.",
  "🚀 Welcome! Let’s make incredible things happen!"
];

const anniversaryMessages = [
  "🎉 Happy Work Anniversary! Your dedication is truly appreciated.",
  "🏆 Cheers to another year of excellence!",
  "🎊 Thank you for being an essential part of our success.",
  "👏 Your commitment and contributions inspire us all!",
  "🥳 Congratulations on your work anniversary!",
  "🌟 Here's to your continued success and growth with us!"
];


document.addEventListener('click', (e) => {
  const btn = e.target.closest('.close-updates');
  if (!btn) return; // not a close click

  const wrapper = document.getElementById('latest-updates-wrapper');
  if (!wrapper) return;

  // animate then hide
  wrapper.classList.remove('show');
  wrapper.style.transition = 'opacity 0.3s';
  wrapper.style.opacity = 0;
  setTimeout(() => {
    wrapper.style.display = 'none';
    wrapper.style.opacity = '';
    wrapper.style.transition = '';
  }, 300);
});



  // Grab elements now
  const openBtn = document.getElementById("open-favourites");
  const favContainer = document.getElementById("fav-cards");
  const modal = document.getElementById("favourites-modal");
  const closeBtn = document.getElementById("close-modal");
  const favList = document.getElementById("favourites-list");
  // Define SVGs per module
const moduleIcons = {
  "HRMS": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <circle cx="10" cy="6" r="4"/>
      <path d="M2 18c0-4 3-6 8-6s8 2 8 6v2H2v-2z"/>
    </svg>`, // 👤 user/head

  "Project": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <rect x="3" y="3" width="14" height="14" rx="2"/>
      <path d="M3 9h14M9 3v14"/>
    </svg>`, // 📊 project grid

  "Buying": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <path d="M6 6h12l-1 9H7L6 6z"/>
      <circle cx="9" cy="18" r="1.5"/>
      <circle cx="15" cy="18" r="1.5"/>
    </svg>`, // 🛒 cart

  "Selling": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <path d="M4 4h12v12H4z"/>
      <path d="M4 9h12M9 4v12"/>
    </svg>`, // 💵 grid/sales

  "Canteen Management": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <path d="M4 2h2v16H4zM10 2h2v16h-2zM16 2h2v16h-2z"/>
    </svg>`, // 🍴 fork/utensil bars

  "Inventory": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <rect x="3" y="3" width="14" height="14" rx="2"/>
      <path d="M3 9h14M9 3v14"/>
    </svg>`, // 📦 box/grid

  "CLMS": `
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor">
      <path d="M2 6h16M2 12h16M2 18h16"/>
    </svg>` // 📑 leave/calendar list
};

  // ✅ Define loadFavouriteCards in this scope
  function loadFavouriteCards() {
    console.log("Loading favourite cards...");
    frappe.call({
      method: "shaher.shaher.page.custom_workspace.custom_workspace.get_fav_documents",
      args:{
        user:frappe.session.user
      },
      callback: function(r) {
        // Clear all except the ➕ card
        favContainer.querySelectorAll(".card-wrapper:not(:first-child)").forEach(el => el.remove());

        if (r.message && r.message.length > 0) {
          r.message.forEach(doc => {
            const wrapper = document.createElement("div");
            
            wrapper.classList.add("card-wrapper");

            wrapper.innerHTML = `
            <style>
  
      .fav_card:hover {
        width: 180px !important;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); 
        z-index: 1;
        background-color: #dce3ff;
        font-weight: 500;
        cursor: pointer;
      }
        .fav_card-hover {
    transition: all 0.3s ease;
  }

  .fav_card-hover:hover {
    width: 160px !important; /* Increase width smoothly */
  }
        </style>
  <div class="fav_card"
       style="background-color:${doc.background_color || '#dce3ff'}; border-radius:12px; padding:16px; width:140px; text-align:center; position:relative;">
    ${doc.icon || `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" 
           width="18" height="18" fill="#1f2937">
        <path d="M406.5 399.6C387.4 352.9 341.5 320 288 320l-64 0c-53.5 0-99.4 32.9-118.5 79.6C69.9 362.2 48 311.7 48 256C48 141.1 141.1 48 256 48s208 93.1 208 208c0 55.7-21.9 106.2-57.5 143.6zm-40.1 32.7C334.4 452.4 296.6 464 256 464s-78.4-11.6-110.5-31.7c7.3-36.7 39.7-64.3 78.5-64.3l64 0c38.8 0 71.2 27.6 78.5 64.3zM256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-272a40 40 0 1 1 0-80 40 40 0 1 1 0 80zm-88-40a88 88 0 1 0 176 0 88 88 0 1 0 -176 0z"/>
      </svg>
    `}
    <div style="margin-top: 20px;">
      <a href="${doc.route}" style="text-decoration:none; color:#000; font-weight:500;">
        ${doc.name}
      </a>
    </div>
  </div>
`;

            favContainer.appendChild(wrapper);
          });
        }
      }
    });
  }

  function loadModalCards() {
  frappe.call({
    method: "shaher.shaher.page.custom_workspace.custom_workspace.get_all_doctypes",
    args: {
      user: frappe.session.user
    },
    callback: function (r) {
      favList.innerHTML = "";
      if (r.message && r.message.length > 0) {
        // Split into favourites & others
        const favourites = r.message.filter(doc => doc.add_to_favourite);
        const others = r.message.filter(doc => !doc.add_to_favourite);

        // --- FAVOURITES ROW ---
        if (favourites.length > 0) {
          const favHeader = document.createElement("h3");
          favHeader.innerText = "Favourites";
          favHeader.style.margin = "8px 0 12px 4px";
          favList.appendChild(favHeader);

          const favRow = document.createElement("div");
          favRow.classList.add("fav-row");
          favRow.style.display = "grid";
          favRow.style.gridTemplateColumns = "repeat(5, 1fr)";
          favRow.style.gap = "16px";
          favourites.forEach(doc => favRow.appendChild(createCard(doc)));
          favList.appendChild(favRow);
        }

        // --- SEARCH BAR ---
        const searchWrapper = document.createElement("div");
        searchWrapper.style.margin = "20px 0";

        const searchInput = document.createElement("input");
        searchInput.type = "text";
        searchInput.placeholder = "Search ...";
        searchInput.style.width = "100%";
        searchInput.style.padding = "10px 14px";
        searchInput.style.borderRadius = "8px";
        searchInput.style.border = "1px solid #ccc";

        searchWrapper.appendChild(searchInput);
        favList.appendChild(searchWrapper);

        // --- MODULE ROWS ---
        const moduleContainer = document.createElement("div");
        favList.appendChild(moduleContainer);

        function renderModules(filterText = "") {
          moduleContainer.innerHTML = "";
          filterText = filterText.toLowerCase();

          // Group by module
          const modules = {};
          others.forEach(doc => {
            const module = doc.modules || "Other";
            if (!modules[module]) {
              modules[module] = [];
            }
            modules[module].push(doc);
          });

          Object.keys(modules).forEach(moduleName => {
            // Filter docs by module name OR doc name
            const filteredDocs = modules[moduleName].filter(doc =>
              moduleName.toLowerCase().includes(filterText) ||
              doc.name.toLowerCase().includes(filterText)
            );

            if (filteredDocs.length === 0) return; // skip empty modules

            // --- MODULE HEADER ---
            const header = document.createElement("h3");
            header.style.display = "flex";
            header.style.alignItems = "center";
            header.style.gap = "8px";
            header.style.margin = "24px 0 12px 4px";
            header.innerHTML = `${moduleIcons[moduleName] || ""} ${moduleName}`;
            moduleContainer.appendChild(header);

            // --- GRID ROW ---
            const row = document.createElement("div");
            row.classList.add("module-row");
            row.style.display = "grid";
            row.style.gridTemplateColumns = "repeat(5, 1fr)";
            row.style.gap = "16px";

            filteredDocs.forEach(doc => {
              row.appendChild(createCard(doc));
            });

            moduleContainer.appendChild(row);
          });
        }

        // Initial render
        renderModules();

        // Search event
        searchInput.addEventListener("input", (e) => {
          const value = e.target.value.trim();
          renderModules(value);
        });
      }
    }
  });
}


// helper function stays same
function createCard(doc) {
  const wrapper = document.createElement("div");
  wrapper.classList.add("card-wrapper");
  const star = doc.add_to_favourite ? "★" : "☆";

  wrapper.innerHTML = `
    <div class="card"
         style="background-color:${doc.background_color || '#dce3ff'}; border-radius:12px; padding:16px; width:140px; text-align:center; position:relative; cursor:pointer;">
      <span class="fav-toggle" data-name="${doc.name}" style="position:absolute; top:8px; right:8px; font-size:18px; cursor:pointer;">${star}</span>
      <div style="margin-top: 20px;">
        <a href="${doc.route}" style="text-decoration:none; color:#000; font-weight:500;">${doc.name}</a>
      </div>
    </div>
  `;

  // Toggle favourite
  wrapper.querySelector(".fav-toggle").addEventListener("click", (e) => {
    const el = e.target;
    const name = el.dataset.name;
    if (el.innerHTML === "☆") {
      el.innerHTML = "★";
      frappe.call({
        method: "shaher.shaher.page.custom_workspace.custom_workspace.add_fav_documents",
        args: { name },
        callback: loadModalCards
      });
      loadFavouriteCards();
    } else {
      el.innerHTML = "☆";
      frappe.call({
        method: "shaher.shaher.page.custom_workspace.custom_workspace.remove_fav_documents",
        args: { name },
        callback: loadModalCards
      });loadFavouriteCards();
    }
  });

  return wrapper;
}



  // ✅ Attach modal open/close
  openBtn.addEventListener("click", () => {
    modal.style.display = "flex";
    loadModalCards();
  });
  closeBtn.addEventListener("click", () => modal.style.display = "none");
  window.addEventListener("click", (event) => {
    if (event.target === modal) modal.style.display = "none";
  });

  // ✅ Call it safely here (function already exists)
  loadFavouriteCards();

  

frappe.call({
  method: 'shaher.shaher.page.custom_workspace.custom_workspace.get_announcements',
  args: { user: frappe.session.user },
  callback: function (r) {
    const updates = r.message || [];
    const wrapper = document.querySelector(".latest-updates-wrapper");
    const container = document.getElementById("latest-updates-list");

    container.innerHTML = '';

    if (!updates.length) {
      const noData = document.createElement("div");
      noData.className = "no-data";
      noData.innerHTML = `
        <h3 style="margin-top: 10px; display:flex; align-items:center; gap:10px; justify-content:left;">
          No announcements available
         
        </h3>
      `;
      //  <span class="close-updates" style="cursor:pointer; font-size:18px; margin-left:auto;" title="Close">✖</span>
      container.appendChild(noData);

      noData.querySelector(".close-updates").addEventListener("click", () => {
        wrapper.classList.remove("show");
        setTimeout(() => (wrapper.style.display = "none"), 300);
      });

      return;
    }

    updates.forEach((note, index) => {
      const card = document.createElement("div");
      card.className = "update-card";
      card.id = `note-${index}`;
      card.style.cursor = "pointer";

      const date = note.creation
        ? frappe.datetime.str_to_obj(note.creation).toLocaleDateString("en-GB", {
            day: "2-digit", month: "short", year: "numeric"
          })
        : "";

      card.innerHTML = `
        <div class="update-header" style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; gap:10px;">
          <div class="update-date">${date}</div>
          <div class="close-btn" style="cursor:pointer; font-size:16px;" title="Dismiss">✖</div>
        </div>
        <div class="update-content">${note.content}</div>
      `;

      // open on click
      card.addEventListener("click", (e) => {
        if (!e.target.classList.contains("close-btn")) {
          frappe.set_route("Form", "Announcements", note.name);
        }
      });

      // dismiss card
      card.querySelector(".close-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        card.style.transition = "opacity 0.3s";
        card.style.opacity = 0;
        setTimeout(() => card.remove(), 300);

        frappe.call({
          method: "shaher.shaher.page.custom_workspace.custom_workspace.mark_announcement_seen",
          args: { announcement_name: note.name, user: frappe.session.user }
        });
      });

      container.appendChild(card);
    });
  }
});



  frappe.call({
    method: "shaher.shaher.page.custom_workspace.custom_workspace.get_workspace_image_for_now",
    callback: function (r) {
      console.log(r)
  const now = new Date();
  const hour = now.getHours();

  let greeting = "Hello";
  const description = r.message?.description || "Let's do great things together.";
  const eventtext = r.message?.event || "";

  let rawPath = r.message?.image || "";
  let imagePath = rawPath.includes("/files/") ? rawPath : "/files/" + rawPath;

  let iconHTML = "";
  const container = document.querySelector('.teampro-container');
  container.classList.remove("theme-morning", "theme-afternoon", "theme-evening", "theme-night");

  if (eventtext == 'Good Morning') {
    greeting = "Good Morning";
    container.classList.add("theme-morning");
    iconHTML = `<div class="cloudPane morning"><div class="sun"></div><div class="toggle-buttons">
      <a href="/app/custom-workspace"><button class="active">Welcome</button></a>
    </div>${cloudsHTML}</div>`;
  } else if (eventtext == 'Good Afternoon') {
    greeting = "Good Afternoon";
    container.classList.add("theme-afternoon");
    iconHTML = `<div class="cloudPane afternoon"><div class="sun bright"></div><div class="toggle-buttons">
      <a href="/app/custom-workspace"><button class="active">Welcome</button></a>
    </div>${cloudsHTML}</div>`;
  } else if (eventtext == 'Good Evening') {
    greeting = "Good Evening";
    container.classList.add("theme-evening");
    iconHTML = `<div class="cloudPane evening"><div class="sun set"></div><div class="toggle-buttons">
      <a href="/app/custom-workspace"><button class="active">Welcome</button></a>
    </div>${cloudsHTML}</div>`;
  } else if (eventtext == 'Good Night'){
    greeting = "Good Night";
    container.classList.add("theme-night");
    iconHTML = `
  <div class="cloudPane night">
    <div class="moon-crescent"></div>
    ${starsHTML}
    <div class="toggle-buttons">
      <a href="/app/custom-workspace"><button class="active">Welcome</button></a>
    </div>
  </div>
`;

  }

  // Update DOM
  document.getElementById("greeting-title").textContent = greeting + ",";
  document.getElementById("greeting-desc").textContent = description;
  document.getElementById("teampro-image").src = imagePath;
  console.log(imagePath)

  const eventElement = document.getElementById("event-message");
  if (eventElement && eventtext) {
    eventElement.innerText = eventtext;
    eventElement.style.display = "block";
  }

  document.getElementById("sunrise-area").innerHTML = iconHTML;
}

  });


// Birthdays
frappe.call({
  method: 'shaher.shaher.page.custom_workspace.custom_workspace.get_today_birthdays',
  callback: function (r) {
    const birthdays = r.message || [];
    const container = $('#birthday-display');

    if (!birthdays.length) {
      container.html(`
  <div class="celebration-card">
    <div class="no-data" style="text-align: center;">
      No birthdays today!
    </div>
  </div>
`);

      return;
    }

    let index = 0;

    function showBirthday() {
      const emp = birthdays[index];
      const imageSrc = (emp.image && emp.image.trim() && emp.image.toLowerCase() !== "null")
        ? emp.image
        : "/files/Blank Image.webp";

      const html = `
        <div class="celebration-card">
          <img 
            src="${imageSrc}" 
            onerror="this.onerror=null;this.src='/files/Blank Image.webp';"
            class="profile-pic"
          />


          <p class="message">Happy Birthday <br><strong>${emp.employee_name}</strong></p>
          <div class="designation">${emp.designation || ''} - ${emp.department || ''}</div>
          <h1 class="emoji">🎉🎁</h1>

          <button class="send-wish-btn"
                  data-emp="${emp.name}"
                  data-emp-name="${emp.employee_name}"
                  data-email="${emp.user_id || ''}"
                  data-type="birthday">
            Send Wish
          </button>
        </div>`;

      container.html(html);

      // Button listeners
      $('.birthday-prev').off('click').on('click', function () {
        index = (index - 1 + birthdays.length) % birthdays.length;
        showBirthday();
      });

      $('.birthday-next').off('click').on('click', function () {
        index = (index + 1) % birthdays.length;
        showBirthday();
      });
    }

    showBirthday();

    // Auto-slide every 60s
    setInterval(function () {
      index = (index + 1) % birthdays.length;
      showBirthday();
    }, 60000);
  }
});


// Joiners

frappe.call({
  method: 'shaher.shaher.page.custom_workspace.custom_workspace.get_today_joiners',
  callback: function (r) {
    const joiners = r.message || [];
    const container = $('#joiners-display');

    if (!joiners.length) {
      container.html(`
  <div class="celebration-card">
    <div class="no-data" style="text-align: center;">
      No new joiners today!
    </div>
  </div>
`); 
      return;
    }

    let index = 0;

    function showJoiner() {
      const emp = joiners[index];
      const imageSrc = (emp.image && emp.image.trim() !== "" && emp.image.toLowerCase() !== "null")
        ? emp.image
        : "/files/Blank Image.webp";

      const html = `
        <div class="celebration-card">
          <img 
            src="${imageSrc}" 
            onerror="this.onerror=null;this.src='/files/Blank Image.webp';"
            class="profile-pic"
          />

          <button class="joiner-prev nav-btn">&lt;</button>
          <button class="joiner-next nav-btn">&gt;</button>

          <p class="message">Welcome <strong>${emp.employee_name}</strong></p>
          <div class="designation">${emp.designation || ''} - ${emp.department || ''}</div>
          <h1 class="emoji">🎊🎉</h1>

          <button class="send-wish-btn"
                  data-emp="${emp.name}"
                  data-emp-name="${emp.employee_name}"
                  data-email="${emp.user_id || ''}"
                  data-type="joiner">
            Send Wish
          </button>
        </div>`;

      container.html(html);

      // Navigation handlers
      $('.joiner-prev').off('click').on('click', function () {
        index = (index - 1 + joiners.length) % joiners.length;
        showJoiner();
      });

      $('.joiner-next').off('click').on('click', function () {
        index = (index + 1) % joiners.length;
        showJoiner();
      });
    }

    showJoiner();

    // Auto-slide every 5s
    setInterval(function () {
      index = (index + 1) % joiners.length;
      showJoiner();
    }, 5000);
  }
});




// Work Anniversaries
frappe.call({
  method: 'shaher.shaher.page.custom_workspace.custom_workspace.get_today_work_anniversaries',
  callback: function (r) {
    const anniversaries = r.message || [];
    const container = $('#anniversary-display');

    if (!anniversaries.length) {
      container.html(`
  <div class="celebration-card">
    <div class="no-data" style="text-align: center;">
      No work anniversaries today!
    </div>
  </div>
`); 
      return;
    }

    let index = 0;

    function showAnniversary() {
      const emp = anniversaries[index];
      const doj = frappe.datetime.str_to_obj(emp.date_of_joining).toLocaleDateString('en-GB');
      const imageSrc = (emp.image && emp.image.trim() !== "" && emp.image.toLowerCase() !== "null")
        ? emp.image
        : "/files/Blank Image.webp";

      const html = `
  <div class="celebration-card">
    <img src="${imageSrc}" onerror="this.onerror=null;this.src='/files/Blank Image.webp';" class="profile-pic" />


    <p class="message">Happy Work Anniversary <br><strong>${emp.employee_name}</strong></p>
    <div class="designation">${emp.designation || ''} - ${emp.department || ''}</div>
    <div class="designation" style="font-size: 12px; color: gray;">Joined on: ${doj}</div>

    <h1 class="emoji">🎉🏅</h1>

    <button class="send-wish-btn"
            data-emp="${emp.name}"
            data-emp-name="${emp.employee_name}"
            data-email="${emp.user_id || ''}"
            data-type="anniversary">
      Send Wish
    </button>
  </div>`;


      container.html(html);

      // Navigation handlers
      $('.anniversary-prev').off('click').on('click', function () {
        index = (index - 1 + anniversaries.length) % anniversaries.length;
        showAnniversary();
      });

      $('.anniversary-next').off('click').on('click', function () {
        index = (index + 1) % anniversaries.length;
        showAnniversary();
      });
    }

    showAnniversary();

    // Auto-slide every 5s
    setInterval(function () {
      index = (index + 1) % anniversaries.length;
      showAnniversary();
    }, 5000);
  }
});






// Send Wish Dialog
window.sendWish = function(empId, userEmail, type, empName = '') {
  let messageOptions = birthdayMessages;
  let subjectPrefix = '🎂 Happy Birthday,';
  let dialogTitle = '🎉 Send a Wish';

  if (type === 'joiner') {
    messageOptions = joinerMessages;
    subjectPrefix = '👋 Welcome Aboard,';
    dialogTitle = '👋 Send Welcome Wish';
  } else if (type === 'anniversary') {
    messageOptions = anniversaryMessages;
    subjectPrefix = '🏅 Happy Work Anniversary,';
    dialogTitle = '🏅 Send Work Anniversary Wish';
  }

  const randomMessages = shuffleArray(messageOptions).slice(0, 6);

  const dialog = new frappe.ui.Dialog({
    title: dialogTitle,
    fields: [
      {
        label: 'Employee',
        fieldname: 'employee',
        fieldtype: 'Link',
        options: 'Employee',
        default: empId,
        read_only: 1
      },
      {
        label: 'Employee Name',
        fieldname: 'employee_name',
        fieldtype: 'Data',
        default: empName,
      },
      {
        label: 'Email',
        fieldname: 'receiver_info',
        fieldtype: 'Link',
        options: 'User',
        default: userEmail,
      },
      {
        label: 'Choose a Wish Message',
        fieldname: 'wish',
        fieldtype: 'Select',
        options: randomMessages,
        default: randomMessages[0]
      },
      {
        label: 'Add a Personal Note (Optional)',
        fieldname: 'personal_note',
        fieldtype: 'Small Text'
      }
    ],
    primary_action_label: 'Send Email',
    primary_action(values) {
      if (!userEmail && !values.receiver_info) {
    frappe.msgprint("No email address available for this employee.");
    dialog.hide();
    return;
  }
  if (!userEmail && values.receiver_info && userEmail !== values.receiver_info) {
    frappe.msgprint("Invalid email address for this employee.");
    dialog.hide();
    return;
  }
  if (userEmail && values.receiver_info && userEmail !== values.receiver_info) {
    frappe.msgprint("Invalid email address for this employee.");
    dialog.hide();
    return;
  }

      frappe.call({
        method: 'shaher.shaher.page.custom_workspace.custom_workspace.send_birthday_wish_email',
        args: {
          user: empId,
          recipients: userEmail,
          subject: `${subjectPrefix} ${empName || empId}!`,
          message: `${values.wish}<br><br>${values.personal_note || ''}`
        },
        callback: function () {
          frappe.msgprint("🎉 Your wish has been sent successfully!");
          dialog.hide();
        }
      });
    }
  });

  dialog.show();
};



// Shuffle array utility
window.shuffleArray = function(array) {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
};







$(document).on('click', '.send-wish-btn', function () {
  const empId = $(this).data('emp');
  const empName = $(this).data('emp-name');
  const userEmail = $(this).data('email');
  const wishType = $(this).data('type');

  sendWish(empId, userEmail, wishType, empName);
});
}






  