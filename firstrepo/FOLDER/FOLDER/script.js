// script.js

document.getElementById("reaction-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const substance1 = document.getElementById("substance1").value;
    const substance2 = document.getElementById("substance2").value;

    // Clear output section
    const reactionDescription = document.getElementById("reaction-description");
    const reactant1Img = document.getElementById("reactant1-img");
    const reactant2Img = document.getElementById("reactant2-img");
    const productImg = document.getElementById("product-img");

    reactionDescription.textContent = "Fetching reaction details...";
    reactant1Img.src = "";
    reactant2Img.src = "";
    productImg.src = "";

    try {
        // Mock API call to fetch reaction details
        const reactionData = await fetchReactionDetails(substance1, substance2);

        if (reactionData) {
            reactionDescription.textContent = reactionData.description;
            reactant1Img.src = reactionData.reactant1Img;
            reactant2Img.src = reactionData.reactant2Img;
            productImg.src = reactionData.productImg;
        } else {
            reactionDescription.textContent = "No reaction found for the given substances.";
        }
    } catch (error) {
        reactionDescription.textContent = "Error fetching reaction details. Please try again.";
        console.error(error);
    }
});

// Simulated API function to fetch reaction details
async function fetchReactionDetails(substance1, substance2) {
    // Replace with actual API calls or logic
    const mockDatabase = {
        "HCl+NaOH": {
            description: "HCl reacts with NaOH to form NaCl and H2O.",
            reactant1Img: "https://via.placeholder.com/100?text=HCl",
            reactant2Img: "https://via.placeholder.com/100?text=NaOH",
            productImg: "https://via.placeholder.com/100?text=NaCl+H2O",
        },
    };

    const key = `${substance1}+${substance2}`;
    return mockDatabase[key] || null;
}
