window.addEventListener(`dragover`, (evt = event) => {
    evt.preventDefault();
    evt.dataTransfer.effectAllowed = `none`;
    evt.dataTransfer.dropEffect = `none`;
}, false);

window.addEventListener(`drop`, (evt = event) => {
    evt.preventDefault();
    evt.dataTransfer.effectAllowed = `none`;
    evt.dataTransfer.dropEffect = `none`;
}, false);
