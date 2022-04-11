eel.expose(showError)
function showError(err) {
    alert(err)
}

eel.expose(showProgress)
function showProgress(progress) {
    document.getElementById('progressBar').value = progress
    document.getElementById('progressBar').innerText = `${progress}%`
}

eel.expose(showResults)
function showResults(profit, ordersDelivered, ordersInProgress, storagePrice) {
    document.getElementById('paramsView').style.display = 'none'
    document.getElementById('progressView').style.display = 'none'
    document.getElementById('resultsView').style.display = 'grid'

    document.getElementById('profitValue').innerText = `${profit} ₽`
    if (profit > 0) {
        document.getElementById('profitValue').classList.remove('loss')
        document.getElementById('profitValue').classList.add('profit')
    } else {
        document.getElementById('profitValue').classList.add('loss')
        document.getElementById('profitValue').classList.remove('profit')
    }
    document.getElementById('ordersDeliveredValue').innerText = `${ordersDelivered}`
    document.getElementById('ordersInProgressValue').innerText = `${ordersInProgress}`
    document.getElementById('storagePriceValue').innerText = `${storagePrice} ₽`
}

eel.expose(printLogs)
function printLogs(logs) {
    let newLogsContent = ''
    for (let date in logs) {
        let logsList = ''
        logsList += `<div>`
        logsList += `<h3>${date}</h3>`
        for (let log of logs[date]) {
            logsList += `
                <div>
                    <span>${log.msg}</span>
                    ${
                        log.profit > 0 ?
                        `<b class="profit">+${log.profit}₽</b>`:
                        (
                            log.profit === 0 ?
                            `` :
                            `<b class="loss">${log.profit}₽</b>`
                        )
                    }
                </div>
            `
        }
        logsList += `</div>`
        newLogsContent += logsList
    }
    document.getElementById('logsList').innerHTML = newLogsContent
}

let medicines = [
    {
        'name': 'Ношпа',
        'code': 'NSP',
        'portion_size': 50,
        'retail_price': 400,
        'demand_price_formula': '-price/80 + 10',
    },
    {
        'name': 'Витамин C',
        'code': 'VTC',
        'portion_size': 100,
        'retail_price': 100,
        'demand_price_formula': '-price/10 + 20',
    },
    {
        'name': 'Витамин D',
        'code': 'VTD',
        'portion_size': 100,
        'retail_price': 150,
        'demand_price_formula': '-price/10 + 30',
    },
    {
        'name': 'Аспирин',
        'code': 'SPR',
        'portion_size': 100,
        'retail_price': 50,
        'demand_price_formula': '-price/10 + 20',
    },
]
function drawMedicines() {
    let newMedicinesListContent = ''
    let i = 0
    for (let med of medicines) {
        newMedicinesListContent += `
            <div class="medicine-card">
                <div class="med_name">
                        <label>Название:</label>
                        <input type="text" value="${med.name}" disabled>
                </div>
                <div class="med_code">
                    <label>Код лекарства:</label>
                    <input type="text" value="${med.code}" disabled>
                </div>
                <div class="med_portion">
                    <label>Размер порции, мг:</label>
                    <input type="number" value="${med.portion_size}" disabled>
                </div>
                <div class="med_price">
                    <label>Цена у поставщика, ₽:</label>
                    <input type="number" value="${med.retail_price}" disabled>
                </div>
                <div class="med_formula">
                    <label>Формула Demand(price):</label>
                    <input type="text" placeholder="Пример: -price/5+40" value="${med.demand_price_formula}" disabled>
                </div>
                <div class="add_del_btn" onclick="removeMedicine(${i})">
                    <div class="button button_red">Удалить</div>
                </div>
            </div>
        `
        i += 1
    }
    newMedicinesListContent += `
        <div class="medicine-card">
            <div class="med_name">
                <label>Название:</label>
                <input type="text" id="newMedicineName">
            </div>
            <div class="med_code">
                <label>Код лекарства:</label>
                <input type="text" id="newMedicineCode">
            </div>
            <div class="med_portion">
                <label>Размер порции, мг:</label>
                <input type="number" id="newMedicinePotionSize">
            </div>
            <div class="med_price">
                <label>Цена у поставщика, ₽:</label>
                <input type="number" id="newMedicinePrice">
            </div>
            <div class="med_formula">
                <label>Формула Demand(price):</label>
                <input type="text" placeholder="Пример: -price/5+40" id="newMedicineDemandPriceFormula">
            </div>
            <div class="add_del_btn">
                <div class="button button_green" id="addMedicineButton">Добавить</div>
            </div>
        </div>
    `
    document.getElementById('medicinesList').innerHTML = newMedicinesListContent
    document.getElementById('addMedicineButton').addEventListener('click', addMedicine)
}
function addMedicine() {
    // TODO: валидация
    medicines.push({
        'name': document.getElementById('newMedicineName').value,
        'code': document.getElementById('newMedicineCode').value,
        'portion_size': document.getElementById('newMedicinePotionSize').value,
        'retail_price': document.getElementById('newMedicinePrice').value,
        'demand_price_formula': document.getElementById('newMedicineDemandPriceFormula').value,
    })
    drawMedicines()
}
function removeMedicine(i) {
    medicines.splice(i, 1)
    drawMedicines()
}

function startModeling() {
    let data = {
        'date_from': document.getElementById('date_from').value,
        'date_to': document.getElementById('date_to').value,
        'budget': document.getElementById('budget').value,
        'margin': document.getElementById('margin').value,
        'expiration_discount': document.getElementById('expiration_discount').value,
        'supply_size': document.getElementById('supply_size').value,
        'couriers_amount': document.getElementById('couriers_amount').value,
        'working_hours': document.getElementById('working_hours').value,
        'medicines': medicines,
    }
    document.getElementById('paramsView').style.display = 'none'
    document.getElementById('progressView').style.display = 'flex'
    document.getElementById('resultsView').style.display = 'none'
    eel.start_modeling(data)
}
document.getElementById('startModelingButton').onclick = startModeling

window.onload = () => drawMedicines()
