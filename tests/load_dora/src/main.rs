// use d_pipeline::{Config, ConfigFormat, read_config_from_file, write_config_to_file};
use d_pipeline::ConfigFormat;

use d_pipeline::format::{read_config_from_file, write_config_to_file};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 读取 YAML 配置
    let config = read_config_from_file("tests/load_dora/dataflow/template.yml", ConfigFormat::Yaml)?;
    
    // 打印所有节点
    for node in config.nodes() {
        println!("Node: {}", node.id);
    }
    
    // 转换为 JSON 格式并保存
    write_config_to_file(&config, "tests/load_dora/dataflow/config.json", ConfigFormat::Json)?;
    
    // 转换为 TOML 格式并保存
    write_config_to_file(&config, "tests/load_dora/dataflow/config.toml", ConfigFormat::Toml)?;
    
    Ok(())
}