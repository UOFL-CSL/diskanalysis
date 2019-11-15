use std::str::FromStr;

pub fn convert_to_int<T>(value: Option<&str>) -> T
where
    T: FromStr,
    <T as FromStr>::Err: std::fmt::Debug,
    T: Default
{
    let conversion = value.expect("0").parse::<T>();

    match conversion {
        Ok(v) => v,
        _ => Default::default()
    }
}