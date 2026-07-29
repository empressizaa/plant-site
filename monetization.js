document.addEventListener("DOMContentLoaded", function () {
// 1. TOP AD PLACEHOLDER (Loads right below the article title)
const topSlot = document.getElementById("ad-top-slot");
if (topSlot) {
topSlot.innerHTML = `
<div style="max-width: 728px; margin: 20px auto; padding: 15px; background-color: #f0f4f1; border: 2px dashed #81c784; border-radius: 6px; text-align: center; font-family: Arial, sans-serif;">
<span style="font-size: 12px; letter-spacing: 1px; color: #4caf50; font-weight: bold; text-transform: uppercase;">[ Advertisement Space ]</span>
<p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">Google AdSense Display Banner will load here.</p>
</div>
`;
}

// 2. BOTTOM SLOT (Stacked: AdSense on top, Amazon Affiliate right below it)
const bottomSlot = document.getElementById("ad-bottom-slot");
if (bottomSlot) {
bottomSlot.innerHTML = `
<div style="max-width: 100%; margin: 30px auto 10px auto; padding: 20px; background-color: #fff; border: 1px solid #e0e0e0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); font-family: Arial, sans-serif; text-align: center;">

<!-- Future AdSense Banner -->
<div style="padding: 15px; background-color: #f9f9f9; border: 1px dashed #ccc; border-radius: 4px; margin-bottom: 20px;">
<span style="font-size: 11px; color: #999; display: block; margin-bottom: 4px;">SPONSORED LINKS</span>
<div style="height: 60px; display: flex; align-items: center; justify-content: center; color: #777; font-size: 14px;">
[ Google AdSense Content Ad ]
</div>
</div>

<hr style="border: 0; border-top: 1px solid #eee; margin: 25px 0;" />

<!-- Future Amazon Affiliate Product Banner -->
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
<span style="font-size: 12px; color: #666; font-weight: bold;">🌱 RECOMMENDED PLANT CARE GEAR</span>
<div style="padding: 15px; width: 100%; max-width: 400px; background: #fffcf5; border: 1px solid #f5e7c4; border-radius: 6px;">
<p style="margin: 0; font-size: 15px; color: #111; font-weight: bold;">[ Amazon Affiliate Link Placeholder ]</p>
<p style="margin: 5px 0 0 0; font-size: 13px; color: #c45500;">★ Recommended Soil Moisture Meter Widget</p>
</div>
</div>

</div>
`;
}
});
