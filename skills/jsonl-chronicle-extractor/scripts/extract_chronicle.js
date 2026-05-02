
const fs = require('fs');
const readline = require('readline');

async function extractChronicles(filePath, pattern) {
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    const regex = new RegExp(pattern);
    let extractedContent = [];

    for await (const line of rl) {
        try {
            const json = JSON.parse(line);
            if (json.message && json.message.content) {
                for (const contentBlock of json.message.content) {
                    if (contentBlock.type === 'text' && contentBlock.text) {
                        if (regex.test(contentBlock.text)) {
                            extractedContent.push(contentBlock.text);
                        }
                    }
                }
            }
        } catch (e) {
            // console.error(`Error parsing line: ${line.substring(0, 100)}...`, e);
            // Non-JSON lines or malformed JSON will be skipped.
        }
    }
    return extractedContent.join('\\n---\\n'); // Separator for multiple chronicles
}

const filePath = process.argv[2];
const pattern = process.argv[3];

if (!filePath || !pattern) {
    console.error('Usage: node extract_chronicle.js <file_path> <regex_pattern>');
    process.exit(1);
}

extractChronicles(filePath, pattern)
    .then(content => {
        if (content) {
            console.log(content);
        } else {
            console.log("No chronicles found matching the pattern.");
        }
    })
    .catch(error => {
        console.error('An error occurred:', error);
        process.exit(1);
    });
