// For use in the web console of https://www.pokencyclopedia.info/en/index.php?id=sprites/gen5/ani_black-white

let dryRun = false;

let extension = "gif";
// let url_pattern = "homeimg";
let suffix = "anim2d";

// Function to get Pokemon index by name
async function getPokemonIndex(name) {
    let response = await fetch(`https://pokeapi.co/api/v2/pokemon/${name}`);
    let data = await response.json();
    return data.id;
}

// Function to get Pokemon name by index
async function getPokemonName(index) {
    let response = await fetch(`https://pokeapi.co/api/v2/pokemon/${index}`);
    let data = await response.json();
    return data.name;
}

// Function to download a file
function downloadFile(url, filename) {
    fetch(url).then(resp => resp.blob()).then(blob => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
    });
}

// Get all normal sprites in the first table
let links = Array.from(document.querySelector('#spr_dump').querySelectorAll(`img`));

// Create a set to keep track of downloaded files
let downloadedFiles = new Set();

// Iterate over each link
let numDownloaded = 0;
let numErr = 0;
let numSkipped = 0;
for (let i = 0; i < links.length; i++) {
    // for (let i = 2; i < 4; i++) {
    let link = links[i];

    // Get the Pokemon name and extra data from the URL
    let url = link.src;
    let linkTail = url.split("/").pop().replace(`.${extension}`, ""); // e.g. ani_bw_001 or ani_bw_003_f

    // Skip -m variants
    if (linkTail.endsWith("_m")) {
        // console.log(`Skipping ${linkTail} because it is a _m variant.`);
        numSkipped++;
        continue;
    }

    // Get just the numeric part of the link tail
    let pokedexNumber = parseInt(linkTail.match(/\d+/)[0]);

    // Get the Pokemon name
    let pokemonName = "UNSET"
    try {
        pokemonName = await getPokemonName(pokedexNumber);
    } catch (error) {
        console.error(`!!! Error getting index for ${name} !!!`);
        numErr++;
        continue;
    }

    // Create the new filename
    let newFilename = `${String(pokedexNumber).padStart(3, '0')}-${pokemonName}-${suffix}.${extension}`;

    // Check if the file has already been downloaded
    if (downloadedFiles.has(newFilename)) {
        console.log(`Skipping ${newFilename} because it has already been downloaded.`);
        numSkipped++;
        continue;
    }

    // Download the file
    if (!dryRun) {
        downloadFile(url, newFilename);
        numDownloaded++;
        downloadedFiles.add(newFilename);

        // Wait for half a second before moving on to the next link
        await new Promise(resolve => setTimeout(resolve, 800));
    }
    else {
        console.log(`Dry run: Download ${newFilename}`);
        // Wait before moving on to the next link
        await new Promise(resolve => setTimeout(resolve, 16));
    }
}
console.log(`Finished downloading ${numDownloaded} files out of ${links.length - numErr - numSkipped} files.\nNumber of links: ${links.length}.\nNumber of skipped files: ${numSkipped}.\nNumber of errors: ${numErr}.`)
