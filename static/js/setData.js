/**
 * This function set the value of a CKEditor box
 * @param {*} box - a CKEditor box
 * @param {*} content - the new content of the box
 */
export function setData(box, content) {
    box.setData(content, {
        callback: function() {
            this.checkDirty();
        }
    });
}