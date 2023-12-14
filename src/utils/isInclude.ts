import { IDate } from "../types/types"

const isInclude = (from: IDate, to:IDate, time: IDate) =>{
    let key: keyof IDate
    let flag1: boolean = true
    let flag2: boolean = true
    
    for (key in time){
      if (from[key] < time[key] ){
        flag1 = true
        break
      }
      if (from[key] > time[key]) {
        flag1 = false
        break
      }
    }
    for (key in time){
      if (to[key] > time[key] ){
        flag2 = true
        break
      }
      if (to[key] < time[key]) {
        flag2 = false
        break
      }
    }
    if (flag1 && flag2){
      return true
    }
    else{
      return false
    }
}

export default isInclude