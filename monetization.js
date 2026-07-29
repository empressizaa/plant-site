/**
* The Plant Matrix - Master Monetization System
* Version 1.0 (Sandbox Mode - Clean Text Active)
*/

window.addEventListener('DOMContentLoaded', () => {
  // 1. SETUP AFFILIATE ROUTING
  // This looks for your green product recommendation link on the page
   const affiliateLinks = document.querySelectorAll('a[href*="/recommend/"]');

  affiliateLinks.forEach(link => {
    // Right now during the sandbox, clicking the link just opens a helpful tip
   link.addEventListener('click', (e) => {
    e.preventDefault();
     alert("Our custom growth tool recommendations are unlocking soon! Check back once our testing phase is complete.");
   });
});

 // 2. SETUP AD SLOTS
 // Ad containers stay completely empty and hidden right now for a premium user experience
 const topAd = document.getElementById('ad-top-slot');
const bottomAd = document.getElementById('ad-bottom-slot');
 if(topAd) topAd.style.display = 'none';
 if(bottomAd) bottomAd.style.display = 'none';
});
