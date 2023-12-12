
export function format_duration(duration) {

    function format_number(t) {
        return t < 10 ? '0' + t : t
    }

    let result = "00:00"
    if (duration > 60) {
        const minutes = Math.floor(duration / 60)
        const seconds = duration - (minutes * 60)
        result = format_number(minutes) + ':' + format_number(seconds)
    } else {
        result = "00:" + format_number(duration)
    }
    return result
}

