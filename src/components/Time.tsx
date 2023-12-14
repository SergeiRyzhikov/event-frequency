import  { FC } from 'react'
import {IDate} from '../types/types'

interface ITimeProps {
    date: IDate
    name: string
    fetchDeleteEvent: (token: string, name: string, time: IDate)=>void
}

const Time:FC<ITimeProps> = ({date, fetchDeleteEvent, name}:ITimeProps) =>{
    const onDeleteEvent=()=>{
        fetchDeleteEvent(String(localStorage.getItem('token')), name, date)
    }
    return(
        <li className='dateCell'>
            {date.year}.{date.month}.{date.day}  {date.hour}:{date.minute} <button className='buttonDeleteEvent'onClick={onDeleteEvent}>X</button>
        </li>
    )
}

export default Time

