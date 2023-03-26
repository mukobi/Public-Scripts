// Console JS for getting the predictions from the AGI Metaculus question
let output = []
for (const [i, prediction] of Object.entries(window.metacData.question.community_prediction.history))
    output.push({ 'date_of_prediction': prediction.time, 'agi_prediction': prediction.x1.q2 * (2200 - 2020) + 2020 })
console.log(output)