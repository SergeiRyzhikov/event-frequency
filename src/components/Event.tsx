import  { FC } from 'react'
import IEvent from '../API/models/ins'
import Time from '../components/Time'
import 'react-calendar-datetime-picker/dist/style.css'
import {IDate} from '../types/types'

interface IEventProps extends IEvent{
    fetchDeleteEvent: (token: string, name: string, time: IDate)=>void
}

const Event:FC<IEventProps> = ({name, time, fetchDeleteEvent}:IEventProps) =>{
    return(
        <div>
            <h4 className='eventHeader'>{name}</h4>
            <ul>{time.map( (date, i)=><Time date={date} fetchDeleteEvent={fetchDeleteEvent} name={name} key={i}/>)}</ul>
        </div>
    )
}

export default Event

