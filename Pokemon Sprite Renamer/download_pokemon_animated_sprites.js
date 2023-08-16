// For use in the web console of https://projectpokemon.org/home/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/

let dryRun = false;

// Function to get Pokemon index by name
async function getPokemonIndex(name) {
    let response = await fetch(`https://pokeapi.co/api/v2/pokemon/${name}`);
    let data = await response.json();
    return data.id;
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
let table = document.querySelector('table');
let links = Array.from(table.querySelectorAll('a[href*="normal-sprite"]'));

// Create a set to keep track of downloaded files
let downloadedFiles = new Set();

// Iterate over each link
let numDownloaded = 0;
let numErr = 0;
let numSkipped = 0;
for (let i = 0; i < links.length; i++) {
    let link = links[i];

    // Get the Pokemon name and extra data from the URL
    let url = link.href;
    let name = url.split("/").pop().replace(".gif", "");
    let [pokemonName, ...extraData] = name.split("-");

    // Replace _ and . with - in the Pokemon name
    pokemonName = pokemonName.replace(/[_\.]/g, "-");

    // Get the Pokemon index
    let index = null;
    let found = false;
    try {
        index = await getPokemonIndex(pokemonName);
    } catch (error) {
        // If getting the index for the split name fails, try the full name
        try {
            index = await getPokemonIndex(name);
            console.log(`Got index for ${name}`)
        } catch (error) {
            // Try adding special names for certain pokemon to conform to the API
            for (let suffix of ["incarnate", "ordinary", "aria", "red-striped", "standard"]) {
                try {
                    index = await getPokemonIndex(`${pokemonName}-${suffix}`);
                    console.log(`Got index for ${pokemonName}-${suffix}`);
                    found = true;
                    break;
                }
                catch (error) {
                    // Don't log the error, just continue to the next suffix
                    continue;
                }
            }
            if (!found) {
                console.error(`!!! Error getting index for ${name} !!!`);
                numErr++;
                continue;
            }
        }
    }

    // Create the new filename
    let newFilename = `${String(index).padStart(3, '0')}-${name}-anim.gif`;

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
}
console.log(`Finished downloading ${numDownloaded} files out of ${links.length - numErr - numSkipped} files.\nNumber of links: ${links.length}.\nNumber of skipped files: ${numSkipped}.\nNumber of errors: ${numErr}.`)
