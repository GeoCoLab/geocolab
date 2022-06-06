import moment, { Moment } from 'moment';
import {StringDict} from '../types';

const expiredMinutes = 5;

export function expired() {
    return moment(moment.now()).subtract(expiredMinutes + 1, 'minutes');
}

export function canUpdate(prev: Moment) {
    return moment.duration(moment().diff(prev)).asMinutes() >= expiredMinutes;
}

export function sortObjectValues(obj: Object) {
    return Object.entries(obj)
        .sort((a, b) => {
            if (a[1] < b[1]) {
                return -1;
            } else if (a[1] > b[1]) {
                return 1;
            }
            return 0;
        }).reduce((result: StringDict, x: Array<string>) => {
            result[x[0]] = x[1];
            return result;
        }, {});
}
