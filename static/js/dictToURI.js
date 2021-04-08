/**
 * Source: https://stackoverflow.com/questions/1714786/query-string-encoding-of-a-javascript-object
 * @param {Object} dict - a dictionary containing information that needs to be encoded 
 * @returns a string encoding dict in URI form 
 */
export function dictToURI(dict) {
    let str = [];
    for(let p in dict){
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dict[p]));
    }
    return str.join("&");
}