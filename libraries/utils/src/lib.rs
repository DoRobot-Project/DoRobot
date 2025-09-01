// crates/utils/src/lib.rs

use std::path::{Path, PathBuf};

// pub fn normalize_path(path: &Path) -> std::io::Result<PathBuf> {
//     if path.is_absolute() {
//         return Ok(path.to_path_buf());
//     }

//     let current_dir = std::env::current_dir()?;
//     let mut absolute_path = current_dir.join(path);

//     // 解析 .. 和 .
//     absolute_path = absolute_path.canonicalize()?;

//     Ok(absolute_path)
// }

use path_clean::PathClean;

pub fn normalize_path<P: AsRef<Path>>(path: P) -> std::io::Result<PathBuf> {
    let path = path.as_ref();

    // println!("Input path: {:?}", path);
    // println!("Is absolute: {}", path.is_absolute());
    
    // if path.is_absolute() {
    //     return Ok(path.clean());
    // }

    // let current_dir = std::env::current_dir()?;
    // let absolute_path = current_dir.join(path);

    // println!("absolute_path path: {:?}", absolute_path);
    
    // Ok(absolute_path.clean())

    let re_path = path.clean();

    println!("re_path: {:?}", re_path);

    Ok(path.clean())
}