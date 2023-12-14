import { IDate } from "../types/types"

const sortDate = (currentEventDates: Array<IDate>) => {
    currentEventDates.sort((a, b)=> {
        let key: keyof IDate
        let flag = 0
        for (key in a){
        if (a[key] < b[key] ){
            flag = -1
            break
        }
        if (a[key] > b[key]) {
            flag = 0
            break
        }
        }
        return flag
    })
    return currentEventDates
}
export default sortDate