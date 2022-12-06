// Enter in chrome console to automatically submit all pending tasks

// modified from https://github.com/gee-hydro/gee_monkey

function runTaskList(){
    $$('.run-button' ,$$('ee-task-pane')[0].shadowRoot).forEach(function(e) {
         e.click();
    })
}

function confirmAll() {
    $$('ee-table-config-dialog').forEach(function(e) {
        var eeDialog = $$('ee-dialog', e.shadowRoot)[0]
        var paperDialog = $$('paper-dialog', eeDialog.shadowRoot)[0]
        var button_div = $$('.buttons', paperDialog)[0]
        $$('.ok-button', button_div)[0].click()
    })
}

runTaskList()
confirmAll()